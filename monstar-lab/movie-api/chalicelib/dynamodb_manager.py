import boto3

class DynamoDBManager:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.movies_table = self.dynamodb.Table('Movies')
        self.favorites_table = self.dynamodb.Table('Favorites')

    def get_movies(self, search_query=None):
        if search_query:
            response = self.movies_table.scan(
                FilterExpression="contains(title, :search)",
                ExpressionAttributeValues={":search": search_query}
            )
        else:
            response = self.movies_table.scan()
        return response['Items']

    def get_movie(self, movie_id):
        response = self.movies_table.get_item(
            Key={'movie_id': movie_id}
        )
        return response.get('Item', None)

    def get_user_favorites(self, user_id):
        response = self.favorites_table.query(
            KeyConditionExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": user_id}
        )
        return response['Items']

    def add_to_favorites(self, user_id, movie_id):
        self.favorites_table.put_item(
            Item={
                'user_id': user_id,
                'movie_id': movie_id
            }
        )
