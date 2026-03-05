import asyncio
import json
import os
import logging
from typing import Dict, Any
from aiokafka import AIOKafkaConsumer
from dotenv import load_dotenv
from .agent import RevOpsAgent

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker-service")

async def main():
    print("Starting RevOps Digital FTE Worker Service (Stage 2: Specialization)...")
    
    # Configuration
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set. Agent may fail.")
    
    kafka_bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = "lead.ingested"

    # Initialize the Agent
    agent = RevOpsAgent(api_key=api_key or "mock-key")
    
    # Initialize Real Kafka Consumer
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=kafka_bootstrap,
        group_id="revops-worker-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="earliest"
    )

    await consumer.start()
    logger.info(f"Connected to Kafka at {kafka_bootstrap}, listening on {topic}")

    try:
        async for msg in consumer:
            logger.info(f"Received lead event: {msg.value.get('email', 'unknown')}")
            try:
                # Process the event with the Agent
                event = msg.value
                audit_result = await agent.run_autonomous_loop(event)
                
                # In a real scenario, we would also produce to 'lead.qualified' here
                # but for now, we just log the successful processing.
                logger.info(f"Successfully processed lead: {event.get('email')}")

            except Exception as e:
                logger.error(f"Error processing lead {msg.value}: {str(e)}")
    finally:
        await consumer.stop()
        logger.info("Kafka Consumer stopped.")

if __name__ == "__main__":
    asyncio.run(main())
