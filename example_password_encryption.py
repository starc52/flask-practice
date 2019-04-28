from passlib.hash import sha256_crypt

passw1= "dfssdfsdf"
passw2 = "sdlfslfsdlf"
passw3= "dfssdfsdf"

print(f"P1 : {passw1}\nP2: {passw2}\nP3: {passw3}")

print("Encrypting..")

passw1 = sha256_crypt.hash(passw1, salt="HA")
passw2 = sha256_crypt.hash(passw2)
passw3 = sha256_crypt.hash(passw3, salt="LS")

print(f"encrypted passwords are")
print(f"P1 : {passw1}\nP2: {passw2}\nP3: {passw3}")

on3 = sha256_crypt.verify("slsl", passw1)
on4 = sha256_crypt.verify("dfssdfsdf", passw1)
print(f"Compare \"slsl\" with 1 is {on3} ")
print(f"Compare \"dfssdfsdf\" with 1 is  {on4}")