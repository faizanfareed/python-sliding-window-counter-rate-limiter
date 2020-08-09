# Sliding Window Counter Rate Limiter
Python sliding window counter API rate limiter using Redis. 





[![Generic badge](https://img.shields.io/badge/license-MIT-success.svg)](https://shields.io/)
[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) 



<a name=""></a>
# Table of contents

- [Why Sliding window counter](#why-sliding-window-counter)
- [Requirements](#requirements)
- [Rate limit strategies](#rate-limit-strategies)
- [Rate limit parameters](#rate-limit-parameters)
- [Usage](#usage)
- [Rate limiter supported methods](#rate-limiter-supported-methods)
- [Optional parameters](#optional-parameters)
- [License](#license)
- [Contributing](#contributing)




# Why Sliding window counter

Sliding window counter is used for two main reasons which are 

- Avoid spikes (smooth out bursts)
- Memory efficient 






# Requirements 
 
- [Python](https://www.python.org/downloads/)
- [Redis](https://redis.io/download)


# Rate limit strategies  

These strategies are used in rate limiter.

- N requests per second 
- N requests per minute
- N requests per hour


# Rate limit parameters

These parameter must be passed when initialize rate limiter class. 

- clientid
- redispipeline
- rate
- time_window_unit 

This **clientid** parameter is used for how many requests serverd for particular user and how many request are left.

This **redispipeline** parameter is redis pipeline which is used for perform opeartions in single shot.


This **rate** parameter is  used for how many request is allowed for particular user.

```python
rate = 100 # 100 request are allowed  
```

This **time_window_unit** parameter  is used for time window. 

```python
# singular time unit allowed. For example 

time_window_unit = 'hour'  
time_window_unit = 'minute'
time_window_unit = 'second'
```

Both **rate** and **time_window_unit** parameters are used for rate limit. Set rate limit

**1400 requests per hour.** 

```python
rate = 1400
time_window_unit = 'hour'
```


**150 requests per minute.** 


```python
rate = 150
time_window_unit = 'minute'
```

**12 requests per second.**


```python
rate = 12
time_window_unit = 'second'
```



# Usage 

Import redis and sliding window counter class

```python
import redis
from  ratelimiter import SlidingWindowCounterRateLimiter
```

Create redis pipeline 
```python        
r = redis.Redis(host='localhost', port=6379, db=1)
pipeline = r.pipeline()
```

We need hourly rate limit for example 300 requests per hour.So initialize rate limiter   



```python    

rate = 300 # 300 requests allowed
time_window_unit = 'hour' # per hour
client_id = 'user-100C' # client id 

# pass these argument into rate limiter
ratelimiter = SlidingWindowCounterRateLimiter(clientid=client_id,redispipeline=pipeline,rate = rate,time_window_unit=time_window_unit)
```


After that check request is allowed or not. 

```python
if ratelimiter.isRequestAllowed(): # Return true if request allowed 
    print('200')

else: # return false if request not allowed
    print('429')
```

# Rate limiter supported methods

Get rate limit HTTP headers.These HTTP headers are returns as a dictionary. 

- X-RateLimit-Limit
- X_RateLimit_Remaining
- **X-RateLimit-Reset** : This header used extra space so if this header set true then it will be part of rate limit http headers otherwise not.
- Retry-after


```python
ratelimiter.getHttpResponseHeaders() # return HTTP response headers as a dictionary.
```





Get **Retry-after** time.

```python
ratelimiter.get_retry_after()
```

Get **X_RateLimit_Remaining**.

```python
ratelimiter.get_x_ratelimit_remaining()
```

Get total request served 

```python
ratelimiter.getTotalRequestServedInSlidingWindow()
```

Get rate limit (max request allowed)

```python
ratelimiter.getMaxRequestsAllowed() 
```

# Optional parameters  

Optional parameters can be passed to rate limiter when first time rate limiter initialized. These parameters are used for performance and reduce memory usage.
 


This **is_ratelimit_reset_header_allowed** parameter is used for X-RateLimit-Reset header which used extra space. If not required then set to false when initialize ratelimiter.

```python
is_ratelimit_reset_header_allowed = True # By default set to true
```

This **is_2nd_RTT_allowed** parameter is used for reduce memory usage and but increase latency. 
Hhen set to true on each request it will delete any expired **Fixed time window** which saved memory but increase latency. 

```python
is_2nd_RTT_allowed = False  # RTT = Round Trip Time
```

This **max_no_time_window_for_deletion** parameter is used for both performance and reduce memory usage. When expired **Fixed time window** reached/euqal to this parameter then 
it will delete all expired **Fixed time windows** and it will ignore is_2nd_RTT_allowed parameter if set to true of false. 

```python

max_no_time_window_for_deletion = 5  # By default set to 5 

```


 




<a name="license"></a>
# License

[![Generic badge](https://img.shields.io/badge/license-MIT-success.svg)](https://shields.io/)

License under a [MIT License](https://choosealicense.com/licenses/mit/).


<a name="contributing"></a>
# Contributing 

- Fork, clone or make a pull requset to this repository. 
- Ask here  [https://github.com/faizanfareed/python-sliding-window-counter-rate-limiter/issues](https://github.com/faizanfareed/python-sliding-window-counter-rate-limiter/issues)
