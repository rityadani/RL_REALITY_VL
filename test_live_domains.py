import requests
import time
from datetime import datetime

def test_live_domains():
    """Test live connection to production domains"""
    domains = {
        'BlackHole Universe': 'https://blackholeinfiverse.com/',
        'Uni-Guru Platform': 'https://www.uni-guru.in/'
    }
    
    print("🔥 Testing LIVE Production Domains...")
    print("=" * 50)
    
    for name, url in domains.items():
        print(f"\n🌐 Testing {name}")
        print(f"URL: {url}")
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                print(f"[OK] Status: CONNECTED")
                print(f"[INFO] Response Time: {response_time}ms")
                print(f"[INFO] HTTP Code: {response.status_code}")
                print(f"[OK] Health: EXCELLENT")
            else:
                print(f"[WARN] Status: CONNECTED (Warning)")
                print(f"[INFO] Response Time: {response_time}ms")
                print(f"[INFO] HTTP Code: {response.status_code}")
                print(f"[WARN] Health: DEGRADED")
                
        except requests.exceptions.Timeout:
            print(f"[ERROR] Status: TIMEOUT")
            print(f"[INFO] Response Time: >10000ms")
            print(f"[ERROR] Health: CRITICAL")
            
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Status: DISCONNECTED")
            print(f"[INFO] Response Time: 0ms")
            print(f"[ERROR] Health: DOWN")
            
        except Exception as e:
            print(f"[ERROR] Status: ERROR")
            print(f"[ERROR] Error: {str(e)}")
            print(f"[ERROR] Health: UNKNOWN")
    
    print("\n" + "=" * 50)
    print(f"[INFO] Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("[INFO] Live dashboard will show real-time status!")

if __name__ == "__main__":
    test_live_domains()