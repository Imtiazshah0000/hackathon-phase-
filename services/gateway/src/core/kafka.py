import json
import os
import logging
from typing import Dict, Any
from aiokafka import AIOKafkaProducer
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("gateway-kafka")

class KafkaProducer:
    """Real Kafka Producer for the Gateway (ADR-2)."""
    
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()
        logger.info(f"Kafka Producer started at {self.bootstrap_servers}")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka Producer stopped.")

    async def publish_lead_ingested(self, lead_data: Dict[str, Any]):
        """Produces a message to the 'lead.ingested' topic."""
        if not self.producer:
            await self.start()
        
        try:
            await self.producer.send_and_wait("lead.ingested", lead_data)
            logger.info(f"[KAFKA] Published to lead.ingested: {lead_data.get('email')}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish to Kafka: {e}")
            return False

# Global Producer Instance
producer = KafkaProducer()
