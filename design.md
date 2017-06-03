##  Key Distribution

```sequence
Alice --> Server: Message(pubk, signature, pubk_of_B, message_1)
Server --> Alice: Ok(signature, sym_key_A_B)
Bob --> Server: Messages(pubk, signature)
Server --> Bob: Ok([(message_1, sym_key_A_B)])
Bob --> Server: Message(pubk_of_B, signature, pubk_of_A, message_2)
Server --> Bob: Recieved(signature)

```



```javascript
// User reprentation on server
// user
{
  public_key: string,
  user_name: string,
  user_status: string,
  messages: [message] // deleted once messages have been acknowledged
}
```

```javascript
// Server state
[user]
```

```javascript
// message
{
  message_id: string
  checksum: int, // based on keys, date, time, messagecontent
  message: string,
  sender_public_key: string,
  reciever_public_key: string,
  timestamp: date
}
```

```javascript
// client_state
{
  addressbook: [client_user],
  private_key: string,
  public_key: string,
  server_public_key: string,
  server_address: string
}
```

```javascript
// client user
{
  public_key: string,
  symetric_key: string,
  messages: [local_message]
}
```

```javascript
// local_message
{
  text: string,
  timestamp: date,
  i_sent: bool
}
```

