# Universal Genius

This project was stated in order to get password self-service reset feature for functional account.

## Getting Started


### Prerequisites

This was created for python 2.7 version due current limitations of destination hosts.

Destination host should have pre-defined ssh keys that will allow you to connect target host (passwordless).

Folder logs should be created


Required modules:

```
pexpect
```


## Built With

* timeout.py - from Stackoverflow, author unknown


## Contributing

Please send email to developer


## Authors

* **Alex Pokushalov** - *Initial work* - [email placeholder here]


## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

## Usage

### Parameters:


Parameter | Help | Example
---|---| ---
list-map | List mapping of DB tnsname to Host:Sid | --list
put | Add/Update mapping of the host:pmon name to DB |  --put DB:host1,port2;host2:port2
delete| Delete mapping| --delete DB
unlock | Just unlock account, no password reset | --unlock
reset | Unlock account and reset password | --reset

