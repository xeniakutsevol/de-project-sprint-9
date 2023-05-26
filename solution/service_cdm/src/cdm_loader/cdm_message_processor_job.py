from datetime import datetime
from logging import Logger

from lib.kafka_connect import KafkaConsumer, KafkaProducer

from cdm_loader.repository.cdm_models import (User_Category_Counters,
                                              User_Product_Counters)
from cdm_loader.repository.cdm_repository import CdmRepository


class CdmMessageProcessor:
    def __init__(
        self,
        consumer: KafkaConsumer,
        producer: KafkaProducer,
        cdm_repository: CdmRepository,
        logger: Logger,
    ) -> None:
        self._consumer = consumer
        self._producer = producer
        self._cdm_repository = cdm_repository
        self._logger = logger
        self._batch_size = 100

    def run(self) -> None:
        self._logger.info(f"{datetime.utcnow()}: START")

        for _ in range(self._batch_size):
            msg = self._consumer.consume()
            if not msg:
                break

            self._logger.info(f"{datetime.utcnow()}: Message received")

            counters_data = msg["payload"]
            user_id = counters_data["user_id"]
            products = [
                User_Product_Counters(
                    user_id=user_id,
                    product_id=obj["id"],
                    product_name=obj["name"],
                    order_cnt=obj["orders_cnt"],
                )
                for obj in counters_data["product"]
            ]
            categories = [
                User_Category_Counters(
                    user_id=user_id,
                    category_id=obj["id"],
                    category_name=obj["name"],
                    order_cnt=obj["orders_cnt"],
                )
                for obj in counters_data["category"]
            ]

            for product in products:
                self._cdm_repository.insert(product)

            for category in categories:
                self._cdm_repository.insert(category)

            self._logger.info(f"{datetime.utcnow()}. Insert to CDM successful")

        self._logger.info(f"{datetime.utcnow()}: FINISH")
