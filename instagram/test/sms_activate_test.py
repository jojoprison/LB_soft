import time

from smsactivateru import Sms, SmsTypes, SmsService, GetBalance, GetFreeSlots, GetNumber

# TODO вставить api sms-active
wrapper = Sms('Aee07A928bbbb7f2104b038d1991ee9e')

# getting balance
balance = GetBalance().request(wrapper)
print(f'На счету {balance} руб.')

# getting free slots (count available phone numbers for each services)
available_phones = GetFreeSlots().request(wrapper)

print('inst.com: {} номеров'.format(available_phones.Instagram.count))

try:
    # try get phone for inst
    activation = GetNumber(
        service=SmsService().Instagram
    ).request(wrapper)
except Exception as e:
    print(e)
    exit(1)

# show activation id and phone for reception sms
print('id: {} phone: {}'.format(str(activation.id), str(activation.phone_number)))

# .. send phone number to you service
user_action = input('Press enter if you sms was sent or type "cancel": ')
if user_action == 'cancel':
    activation.cancel()
    exit(1)

while True:
    try:
        # set current activation status as SmsSent (code was sent to phone)
        print(activation.was_sent())
        break
    except Exception as e:
        print(e)
        print('sleep 4 seconds')
        time.sleep(4)


# callback method for eval (if callback not set, code will be return)
def fuck_yeah(code):
    print('Oh, it\'s my code! {}'.format(code))


# .. wait code
activation.wait_code(callback=fuck_yeah, wrapper=wrapper, not_end=True)

print('this string print before eval fuck_yeah function')

# .. and wait one mode code
# (!) if you not set not_end (or set False) – activation ended before return code
activation.wait_code(callback=fuck_yeah, wrapper=wrapper)
