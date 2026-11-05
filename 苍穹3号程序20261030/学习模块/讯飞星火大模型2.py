from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = '6453e52c'
SPARKAI_API_SECRET = 'MDYzMGRjMzNlNDU0YzM1MzRiYTlkYWVj'
SPARKAI_API_KEY = 'ffa30420efed3f39f266221e36863873'
#星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'

if __name__ == '__main__':
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(
        role="user",
        content=("#角色：你是一个通晓各领域的专家"
                 "#任务：接下来用户会问你做某些事情前的必要步骤有哪些，你需要具体回答"
                "#回答格式:回答中的每个步骤用中文逗号隔开，回答中不要出现其他任何内容，回答的末尾不要加句号"
                "用户：实现螺旋藻采收的自动化前的必要步骤有哪些")
    )]
    
    handler = ChunkPrintHandler()
    response = spark.generate([messages], callbacks=[handler]).generations[0][0].text
    print(response)
    
