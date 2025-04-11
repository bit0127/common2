Environment setting for windows 10, AWS:
1. Install VScode
2. Install python(3.11.9) in machine
3. Then install chalice framwork (chalice 1.31.3)
4. Pull the source code from from git
5. First open dynamodb-manager project
6. Then from the terminal run "pip install -r requirements.txt ", that will install required library
7. First configure local aws region, aws_access_key_id, aws_secret_access_key. I use 'aws configure' command from vs code terminal.
7. Go to AWS console and create a role that can invoke lambda, create delete edit API, dynabo db access and create, secret manager read write permission (As it is my own AWS, I full access for lambda, API, DB, secret manager)
8. Then copy this role 'ARN' and put it inside config.json file. we can see 'write-your-iam_role-arn', just replace it.
9. Then 'chalice deploy' will deploy required lambda. Then from aws console manually run 'create-db', 'insert-dummy-movies', 'insert-dummy-user'. Then it will populate dummy data.
10. Now open another project "movie-api" with vscode
11. Then from the terminal run "pip install -r requirements.txt ", that will install required library
12. Now again copy that previous role ARN and paste it in config.json file. we can see 'write-your-iam_role-arn', just replace.
13. Now again go to AWS console. Go to secret manager and put a key value pair. Give key name "JWT_SECRET_KEY" and value "afecbc4633dd0ec41741a77b36ca4e3dea0516de3e629b67bf4923ec6d52ca2e". we can make make secret key in different way. I make it using python 'secret' library.
14. Now 'chalice deploy' command will deploy this API through AWS API gateway and a api url will see in terminal. But we can also copy this url from AWS API gateway.

Here I am writing how we can test API now (I use postman, because we don't have UI):

15. Now we can copy the api url and with this url+ '/movies' will show the movie list in browser
(For me: https://mr7araxkdg.execute-api.ap-northeast-1.amazonaws.com/api/movies we can run), 
url+movies/id will show specific movie (https://mr7araxkdg.execute-api.ap-northeast-1.amazonaws.com/api/movies/2)
16. Login API: url + /login (for me: https://mr7araxkdg.execute-api.ap-northeast-1.amazonaws.com/api/login). In postman,Write raw body like {"user_id": "user1"}  will generate token for login user user1. Then run it and copy token.
17. Favorites API: url + /favorites/id (for me: https://mr7araxkdg.execute-api.ap-northeast-1.amazonaws.com/api/favorites/1), In postman we can set 'Authorization' key in headers then put value Bearer 'copied token' and send. My url will add movie where id is 1 for that login user.
18. Now url + /favorites will show the movies for login user. (for me:https://mr7araxkdg.execute-api.ap-northeast-1.amazonaws.com/api/favorites). Here we can use same token as bearer. (Keep in mind I put token expire time 1 hour)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Improvement points:
 1. I think I can write this program more object oriented way. For an example, In Movie-API project I wrote DynamoDBManager class in chalicelib by following OOP (class, instance varible) rules. But I didn't follow that always because of time.
 2. May be no need, but just for precaution may be other library need to install as my personal compter already a complete setup. So it will show python library ;module not found' error at the time of deployment, just copy that not found library and run command "pip install 'that not found'". 