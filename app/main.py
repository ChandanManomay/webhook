from flask import Flask, request, Response
import urllib3

app = Flask(__name__)

token ='EAALZBR0QxzHgBANZAyl99o74jsO9NqVUC49GH9L0zEPJUXdRxhhInOQd6O9xZANJJpaXhOKDkivCZCPeaqEKmBIs6R73aZB0REPFB18566gfnkZCMutrk4bBEp0AhRmWKjpeCrCOelbnRd5Bt2koggwCg8qPKDadh01cgrMZBRW3m12YB7ZBJ27T5aPtESxxixeJwrHFk7cra2OKryLvt3G6'
my_token = "Chandan"

@app.route("/")
def welcome():
    return '<h1> Welcome in Webhook</h1>'

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    app.logger.info(request)
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        v_token = request.args.get("hub.verify_token")
        app.logger.info(mode)
        if mode and v_token:
            if mode=="subscribe" and v_token == my_token:
                return Response(challenge,status=200)
        return Response(status=403)

       
    elif request.method == "POST":
        body_perm = request.json
        print(body_perm)
        object = body_perm["object"]
        entry = body_perm['entry']
        changes = entry[0]['changes']
        value = changes[0]['value']
        messages = value["messages"]

        if object:
            if entry and changes and value and messages and messages[0]:
                phone_no_id = value["metadata"]["phone_number_id"]
                from_ = messages[0]['from']
                msg_body = messages[0]['text']['body']
                print(msg_body)
                http = http = urllib3.PoolManager()
                url = "https://graph.facebook.com/v15.0/"+phone_no_id+"/messages?access_token"+token
                data = {
                    "messaging_product": "whatsapp",
                    "to":from_,
                    "text": {
                    "body": "Hi I am Chandan"
                  }
                }
                header={
                    "Content-Type": "application/json"
                }
                res = http.request("POST",url,data=data,headers=header)
                return Response(res)
            return Response(status=404)