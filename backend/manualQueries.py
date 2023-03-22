import user.queries as queries
import user.views.account as accUtil

username = "Arnav"
password = "123"
phone = "+13176909263"
queries.createUser(
    username,
    passwordHash=accUtil.getPasswordHash(password, username),
    phoneNumber=phone
)