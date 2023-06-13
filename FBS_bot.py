from token_fbs_bot import TOKIN
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
from markups import genmarkup

from get_zakaz_OZON import pars_date_OZON, send_request

bot = Bot(token=TOKIN, parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands="start") # стартовое приветствие бота.
async def cmd_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Приветствую вас: {0.first_name}'.format(message.from_user), reply_markup=nav.mainMenu) # приведствует и добавляет кнопку
    
@dp.message_handler(commands=['OZON_FBS']) # перенаправляет в подменю OZON
async def ozon_fbs(message: types.Message):
    await bot.send_message(message.from_user.id, 'OZON_FBS'.format(message.from_user), reply_markup=nav.menuzakaz)
    
@dp.message_handler(commands=['Сборки_OZON']) # предоставляет данные для заказов которые нужно собрать 
async def zak_ozon_fbs(message: types.Message):
    await bot.send_message(message.from_user.id, "Ждите {0.first_name}, идет сбор данных.".format(message.from_user)) # просто просит подождать
    data_OZON_FBS = pars_date_OZON()                                                                                  # запускает процесс сбора данных 
    for index, item in enumerate(data_OZON_FBS[2]):                                                                   # передирает данные и анализирует какие нужно 
        if item == "Заказов нет":                                                                                     # отправить клиенту с кнопкой по сборке
            await bot.send_message(
                message.from_user.id,
                "Заказов нет, попробуйте проверить позднее.".format(
                    message.from_user
                ),
            )
        elif item == "ожидает упаковки":                                                                              # отправляет пользователю все данные для сборки заказа со склада
            await bot.send_message(
                message.from_user.id,
                f"Принят в обработку: \n {data_OZON_FBS[0][index]} \n\n Номер отправления: \n {data_OZON_FBS[1][index]} \n\n Статус: \n {data_OZON_FBS[2][index]} \n\n Дата отгрузки: \n {data_OZON_FBS[3][index]} \n\n Состав отправления: \n {data_OZON_FBS[4][index]} \n {data_OZON_FBS[5][index]} \n\n Стоимость: \n {data_OZON_FBS[6][index]} \n\n Склад: \n  {data_OZON_FBS[7][index]} \n\n Служба доставки и метод \n {data_OZON_FBS[8][index]} \n\n\n\n ОГАРНИЧЕНИЯ СКЛАДА: \n\n Ограничение по максимальному весу в граммах. \n {data_OZON_FBS[10][0][index]} \n\n Ограничение по ширине в сантиметрах. \n {data_OZON_FBS[10][1][index]} \n\n Ограничение по длине в сантиметрах. \n {data_OZON_FBS[10][2][index]} \n\n Ограничение по высоте в сантиметрах. \n {data_OZON_FBS[10][3][index]} \n\n Ограничение по максимальной стоимости отправления в рублях. \n {data_OZON_FBS[10][4][index]}".format(
                    message.from_user), reply_markup=genmarkup(data_OZON_FBS[1][index]))

@dp.message_handler(commands=['Отгрузки_OZON']) # предоставляет данные для заказов которые нужно отправить 
async def otprav_ozon_fbs(message: types.Message):
    await bot.send_message(message.from_user.id, "Ждите {0.first_name}, идет сбор данных.".format(message.from_user))
    data_OZON_FBS = pars_date_OZON()
    for index, item in enumerate(data_OZON_FBS[2]):
        if item == "Заказов нет":
            await bot.send_message(
                message.from_user.id,
                "Заказов нет, попробуйте проверить позднее.".format(
                    message.from_user
                ),
            )
        elif item == "ожидает отгрузки":                                                                               # отправляет пользователю все данные для отправки заказа со склада
            await bot.send_message(
                message.from_user.id,
                f"Принят в обработку: \n {data_OZON_FBS[0][index]} \n\n Номер отправления: \n {data_OZON_FBS[1][index]} \n\n Статус: \n {data_OZON_FBS[2][index]} \n\n Дата отгрузки: \n {data_OZON_FBS[3][index]} \n\n Состав отправления: \n {data_OZON_FBS[4][index]} \n {data_OZON_FBS[5][index]} \n\n Стоимость: \n {data_OZON_FBS[6][index]} \n\n Склад: \n  {data_OZON_FBS[7][index]} \n\n Служба доставки и метод \n {data_OZON_FBS[8][index]} \n\n\n\n ОГАРНИЧЕНИЯ СКЛАДА: \n\n Ограничение по максимальному весу в граммах. \n {data_OZON_FBS[10][0][index]} \n\n Ограничение по ширине в сантиметрах. \n {data_OZON_FBS[10][1][index]} \n\n Ограничение по длине в сантиметрах. \n {data_OZON_FBS[10][2][index]} \n\n Ограничение по высоте в сантиметрах. \n {data_OZON_FBS[10][3][index]} \n\n Ограничение по максимальной стоимости отправления в рублях. \n {data_OZON_FBS[10][4][index]}".format(
                    message.from_user), reply_markup=genmarkup(data_OZON_FBS[1][index]))
            
@dp.message_handler(commands=['Назад']) # команда для возврата к предыдущему меню
async def back_ozon_fbs(message: types.Message):
    await bot.send_message(message.from_user.id, "Возврат в предыдущее меню.".format(message.from_user), reply_markup=nav.mainMenu)
            
@dp.callback_query_handler(lambda call: True)  # отправляет команду к API OZON что заказ собран.
async def stoptopupcall(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    send_request(callback_query.data)
    await bot.send_message(callback_query.from_user.id, f"Собран {callback_query.data}")       


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
