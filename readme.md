## Home made Gwent Api - keep track of the cards you have in your collection

### General responses

```json
[
    "data" : "response content",
    "message" : "what happened on 'server'"
]
```

### Getting cards

`GET /cardlist` -> return cards stored
`GET /cardlist/<name>` -> return card by name

Returns `200 OK`

```json
{
    "message": "Success",
    "data": [
        {
            "name": "Poor Fucking Infantry",
            "card_type": "unit",
            "ability": "none",
            "description": "",
            "row" : "melee",
            "stregnth" : "1",
            "faction" : "neutral"
        }
    ]
    ...
}
```

404 Not Found if doesn't exist in DB

An error will be thrown if the card exists already. 

Note: if you want to add a card with same name, call PUT and specify the update quantity

### Adding a new card 
`POST /cardlist`

```json
{
    "name": "Poor Fucking Infantry",
    "card_type": "unit",
    "ability": "none",
    "description": "null",
    "row" : "melee",
    "stregnth" : "1",
    "faction" : "neutral",
    "quantity" : "0"
}
```
The above are all required values. If some are missing, a 400 error is returned

```json
{
    "message": {
        "ability": "Missing required parameter in the JSON body or the post body or the query string"
    }
}
```
If the card you are wanting to add doesn't need a particular field, specify `null`. E.g. a weather card won't have a strength value, similarly a neutral card type won't have a faction

### Deleting a card

`DELETE` /carditem/<name:string>

If successful, a 204 is returned

```json
{'message' : 'card deleted'}
```

If the card isn't found, it is a 404 is returned. 

NB: the deletion will subtract its quantity if more than one card found for the same name

### Updating a card

`PUT` /carditem/<string:name>

Will return 200 OK or 400 if the card does not exist. You will want to specify all the fields since it will simply overwrite the existing card

```json
{
    "name": "Poor Fucking Infantry",
    "card_type": "unit",
    "ability": "none",
    "description": "null",
    "row" : "melee",
    "stregnth" : "1",
    "faction" : "neutral",
    "quantity" : "0"
}
```