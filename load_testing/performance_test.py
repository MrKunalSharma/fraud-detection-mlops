import asyncio
import aiohttp
import time
import json
import numpy as np
from datetime import datetime
import statistics

class LoadTester:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.results = []
        
    async def make_request(self, session, transaction_data):
        """Make a single API request"""
        start_time = time.time()
        
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            async with session.post(
                f"{self.api_url}/predict",
                json=transaction_data,
                headers=headers
            ) as response:
                result = await response.json()
                latency = time.time() - start_time
                
                return {
                    "status": response.status,
                    "latency": latency,
                    "model_version": result.get("model_version"),
                    "prediction": result.get("prediction"),
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "status": "error",
                "latency": time.time() - start_time,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_transaction(self, fraud_probability=0.1):
        """Generate random transaction data"""
        is_fraud = np.random.random() < fraud_probability
        
        if is_fraud:
            # Fraud pattern
            return {
                "Time": np.random.uniform(0, 100000),
                "Amount": np.random.uniform(1000, 10000),
                **{f"V{i}": np.random.uniform(-10, 10) for i in range(1, 29)}
            }
        else:
            # Normal pattern
            return {
                "Time": np.random.uniform(0, 10000),
                "Amount": np.random.uniform(1, 500),
                **{f"V{i}": np.random.normal(0, 1) for i in range(1, 29)}
            }
    
    async def run_load_test(self, num_requests: int, concurrency: int):
        """Run load test with specified concurrency"""
        print(f"Starting load test: {num_requests} requests with {concurrency} concurrent connections")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for i in range(num_requests):
                transaction = self.generate_transaction()
                task = self.make_request(session, transaction)
                tasks.append(task)
                
                # Limit concurrency
                if len(tasks) >= concurrency:
                    results = await asyncio.gather(*tasks)
                    self.results.extend(results)
                    tasks = []
            
            # Handle remaining tasks
            if tasks:
                results = await asyncio.gather(*tasks)
                self.results.extend(results)
        
        self.analyze_results()
    
    def analyze_results(self):
        """Analyze and display load test results"""
        successful_requests = [r for r in self.results if r.get("status") == 200]
        failed_requests = [r for r in self.results if r.get("status") != 200]
        
        latencies = [r["latency"] for r in successful_requests]
        
        print("\n" + "="*50)
        print("LOAD TEST RESULTS")
        print("="*50)
        
        print(f"\nTotal Requests: {len(self.results)}")
        print(f"Successful: {len(successful_requests)}")
        print(f"Failed: {len(failed_requests)}")
        print(f"Success Rate: {len(successful_requests)/len(self.results)*100:.2f}%")
        
        if latencies:
            print(f"\nLatency Statistics (seconds):")
            print(f"  Min: {min(latencies):.3f}")
            print(f"  Max: {max(latencies):.3f}")
            print(f"  Mean: {statistics.mean(latencies):.3f}")
            print(f"  Median: {statistics.median(latencies):.3f}")
            print(f"  95th Percentile: {np.percentile(latencies, 95):.3f}")
            print(f"  99th Percentile: {np.percentile(latencies, 99):.3f}")
        
        # Model version distribution (A/B testing results)
        model_versions = [r.get("model_version") for r in successful_requests if r.get("model_version")]
        if model_versions:
            print(f"\nModel Version Distribution:")
            for version in set(model_versions):
                count = model_versions.count(version)
                percentage = count / len(model_versions) * 100
                print(f"  {version}: {count} ({percentage:.1f}%)")
        
        # Save detailed results
        with open("load_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_requests": len(self.results),
                    "successful": len(successful_requests),
                    "failed": len(failed_requests),
                    "success_rate": len(successful_requests)/len(self.results)*100,
                    "avg_latency_ms": statistics.mean(latencies) * 1000 if latencies else 0,
                    "p95_latency_ms": np.percentile(latencies, 95) * 1000 if latencies else 0,
                    "p99_latency_ms": np.percentile(latencies, 99) * 1000 if latencies else 0
                },
                "details": self.results
            }, f, indent=2)
        
        print(f"\nDetailed results saved to load_test_results.json")

async def main():
    # Configuration
    API_URL = "https://fraud-detection-api-v5cc.onrender.com"
    API_KEY = "demo-key-123"
    
    # Test scenarios
    scenarios = [
        {"name": "Light Load", "requests": 100, "concurrency": 10},
        {"name": "Medium Load", "requests": 500, "concurrency": 50},
        {"name": "Heavy Load", "requests": 1000, "concurrency": 100}
    ]
    
    tester = LoadTester(API_URL, API_KEY)
    
    for scenario in scenarios:
        print(f"\n\nRunning scenario: {scenario['name']}")
        await tester.run_load_test(scenario['requests'], scenario['concurrency'])
        
        # Wait between scenarios
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
