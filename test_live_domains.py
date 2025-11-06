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
                print(f"✅ Status: CONNECTED")
                print(f"⚡ Response Time: {response_time}ms")
                print(f"📊 HTTP Code: {response.status_code}")
                print(f"🎯 Health: EXCELLENT")
            else:
                print(f"⚠️ Status: CONNECTED (Warning)")
                print(f"⚡ Response Time: {response_time}ms")
                print(f"📊 HTTP Code: {response.status_code}")
                print(f"🎯 Health: DEGRADED")
                
        except requests.exceptions.Timeout:
            print(f"❌ Status: TIMEOUT")
            print(f"⚡ Response Time: >10000ms")
            print(f"🎯 Health: CRITICAL")
            
        except requests.exceptions.ConnectionError:
            print(f"❌ Status: DISCONNECTED")
            print(f"⚡ Response Time: 0ms")
            print(f"🎯 Health: DOWN")
            
        except Exception as e:
            print(f"❌ Status: ERROR")
            print(f"🔥 Error: {str(e)}")
            print(f"🎯 Health: UNKNOWN")
    
    print("\n" + "=" * 50)
    print(f"🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 Live dashboard will show real-time status!")

if __name__ == "__main__":
    test_live_domains()