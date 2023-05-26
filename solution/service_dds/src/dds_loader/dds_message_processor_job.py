from datetime import datetime
from logging import Logger

from lib.kafka_connect import KafkaConsumer, KafkaProducer

from dds_loader.repository.dds_order_builder import DdsOrderBuilder
from dds_loader.repository.dds_repository import DdsRepository


class DdsMessageProcessor:
    def __init__(
        self,
        consumer: KafkaConsumer,
        producer: KafkaProducer,
        dds_repository: DdsRepository,
        logger: Logger,
    ) -> None:
        self._consumer = consumer
        self._producer = producer
        self._dds_repository = dds_repository
        self._logger = logger
        self._batch_size = 30

    def run(self) -> None:
        self._logger.info(f"{datetime.utcnow()}: START")

        for _ in range(self._batch_size):
            msg = self._consumer.consume()
            if not msg:
                break

            self._logger.info(f"{datetime.utcnow()}: Message received")

            order = msg["payload"]
            order_builder = DdsOrderBuilder(order)
            self._dds_repository.insert(order_builder.h_user())
            for i in order_builder.h_product():
                self._dds_repository.insert(i)
            for i in order_builder.h_category():
                self._dds_repository.insert(i)
            self._dds_repository.insert(order_builder.h_restaurant())
            self._dds_repository.insert(order_builder.h_order())
            for i in order_builder.l_order_product():
                self._dds_repository.insert(i)
            for i in order_builder.l_product_restaurant():
                self._dds_repository.insert(i)
            for i in order_builder.l_product_category():
                self._dds_repository.insert(i)
            self._dds_repository.insert(order_builder.l_order_user())
            self._dds_repository.insert(order_builder.s_user_names())
            for i in order_builder.s_product_names():
                self._dds_repository.insert(i)
            self._dds_repository.insert(order_builder.s_restaurant_names())
            self._dds_repository.insert(order_builder.s_order_cost())
            self._dds_repository.insert(order_builder.s_order_status())

            self._logger.info(f"{datetime.utcnow()}. Insert to DDS successful")

            user_id = str(order_builder.h_user().h_user_pk)
            products = [
                {"id": str(obj[1]), "name": obj[2], "orders_cnt": obj[3]}
                for obj in self._dds_repository.counter(user_id, "product")
            ]
            categories = [
                {"id": str(obj[1]), "name": obj[2], "orders_cnt": obj[3]}
                for obj in self._dds_repository.counter(user_id, "category")
            ]

            output_message = {
                "object_id": user_id,
                "object_type": "user_product_category_counters",
                "payload": {
                    "user_id": user_id,
                    "product": products,
                    "category": categories,
                },
            }

            self._producer.produce(output_message)
            self._logger.info(f"{datetime.utcnow()}. Message sent")

        self._logger.info(f"{datetime.utcnow()}: FINISH")
