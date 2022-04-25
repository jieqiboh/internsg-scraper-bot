#basic imports and error logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
#Connect to database and return client object
import pymongo
from pymongo import MongoClient

#takes name of category (name of collection in db) and returns items in list format
def returnCategoryList(category):
    #category must be "job_ids" or "company" or "title" or "period" or "job_type"
    conn_str = "mongodb+srv://admin:admin@cluster0.6ejza.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(conn_str)
    value = "item" if category!="job_ids" else "job_details"
    
    return list(key[value] for key in client["mydatabase"][category].find({},{"_id":0}))

def returnCategoryListMsg(category):
    lst = returnCategoryList(category)
    msg = ""
    for i in range(len(lst)):
        msg+=str(i+1)+". "+str(lst[i])+"\n"
    return msg

#checks if entryName is in collection and removes it and returns "removed!", else returns "entry not found in database!"
def removeFromCategory(collectionName,entryName):
    #category must be "job_ids" or "company" or "title" or "period" or "job_type"
    conn_str = "mongodb+srv://admin:admin@cluster0.6ejza.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(conn_str)
    
    collection = client["mydatabase"][collectionName]
    
    find_entry = collection.find_one({'item':entryName})
    if find_entry:
        collection.delete_one({'item':entryName})
        return True
    else:
        return False

#checks if entryName is in collection and removes it and returns "removed!", else returns "entry not found in database!"
def addToCategory(collectionName,entryName):
    #category must be "job_ids" or "company" or "title" or "period" or "job_type"
    conn_str = "mongodb+srv://admin:admin@cluster0.6ejza.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(conn_str)
    
    collection = client["mydatabase"][collectionName]
    
    find_entry = collection.find_one({'item':entryName})
    if not find_entry:
        collection.insert_one({'item':entryName})
        return True
    else:
        return False

TOKEN = '5285656526:AAFAL9iXqQf-8XToM0nnEByG46zfQ2Rmmq8'
TELEGRAM_URL = "https://api.telegram.org/bot" + TOKEN
############################### Bot ############################################
def start(update, context):
    update.message.reply_text(main_menu_message(),reply_markup=main_menu_keyboard())

def main_menu(update, context):
    update.callback_query.message.edit_text(main_menu_message(),reply_markup=main_menu_keyboard())

#PREFERENCES
def preferences_menu(update, context):
    print(update)
    print(context)
    update.callback_query.message.edit_text(preferences_menu_message(),reply_markup=preferences_menu_keyboard())
#
def addremoveCompany_menu(update, context):
    update.callback_query.message.edit_text(addremove_menu_message(),reply_markup=addremoveCompany_menu_keyboard())
    
def addcompany_ftn(update, context):
    context.user_data['collectionName'] = "company"
    context.user_data['addremove'] = "add"
    dispatcher.add_handler(allMessageHandler)
    update.callback_query.message.edit_text(add_menu_message() +"\n"+ returnCategoryListMsg("company"))
    
def removecompany_ftn(update, context):
    context.user_data['collectionName'] = "company"
    context.user_data['addremove'] = "remove"
    dispatcher.add_handler(allMessageHandler)
    update.callback_query.message.edit_text(remove_menu_message() +"\n"+ returnCategoryListMsg("company"))

def addremoveTitle_menu(update, context):
    update.callback_query.message.edit_text(addremove_menu_message(),reply_markup=addremoveTitle_menu_keyboard())
    
def addtitle_ftn(update, context):
    context.user_data['collectionName'] = "title"
    context.user_data['addremove'] = "add"
    dispatcher.add_handler(allMessageHandler)
    update.callback_query.message.edit_text(add_menu_message() +"\n"+ returnCategoryListMsg("title"))
    
def removetitle_ftn(update, context):
    context.user_data['collectionName'] = "title"
    context.user_data['addremove'] = "remove"
    dispatcher.add_handler(allMessageHandler)
    update.callback_query.message.edit_text(remove_menu_message() +"\n"+ returnCategoryListMsg("title"))
#
def addremovePeriod_menu(update, context):
    update.callback_query.message.edit_text(addremove_menu_message(),reply_markup=addremovePeriod_menu_keyboard())
    
def addperiod_ftn(update, context):
    context.user_data['collectionName'] = "period"
    context.user_data['addremove'] = "add"
    dispatcher.add_handler(allMessageHandler)
    update.callback_query.message.edit_text(add_menu_message() +"\n"+ returnCategoryListMsg("period"))
    
def removeperiod_ftn(update, context):
    context.user_data['collectionName'] = "period"
    context.user_data['addremove'] = "remove"
    dispatcher.add_handler(allMessageHandler)
    update.callback_query.message.edit_text(remove_menu_message() +"\n"+ returnCategoryListMsg("period"))
#
def addremoveJobType_menu(update, context):
    update.callback_query.message.edit_text(addremove_menu_message(),reply_markup=addremoveJobType_menu_keyboard())
    
def addjobtype_ftn(update, context):
    context.user_data['collectionName'] = "job_type"
    context.user_data['addremove'] = "add"
    dispatcher.add_handler(allMessageHandler)
    update.callback_query.message.edit_text(add_menu_message() +"\n"+ returnCategoryListMsg("job_type"))
    
def removejobtype_ftn(update, context):
    context.user_data['collectionName'] = "job_type"
    context.user_data['addremove'] = "remove"
    dispatcher.add_handler(allMessageHandler)
    update.callback_query.message.edit_text(remove_menu_message() +"\n"+ returnCategoryListMsg("job_type"))
    
#END OF PREFERENCES
def scrapedpostings_menu(update, context):
    print(update)
    job_details = returnCategoryList("job_ids")
    for job in job_details:
        msg = ""
        for item in job.items():
            msg+=item[0]+": "+item[1]+"\n"
        context.bot.send_message(chat_id=update.effective_chat.id,text=msg)

def botdetails_menu(bot, update):
    bot.callback_query.message.edit_text(botdetails_message())
    
def addkeyword_message_ftn(bot, update):
    bot.callback_query.message.edit_text(add_menu_message())
    
def removekeyword_message_ftn(bot, update):
    bot.callback_query.message.edit_text(remove_menu_message())

def error(update, context):
    print(f'Update {update} caused error {context.error}')
    
#CONVERSATION HANDLER FTNS
def addremove_input(update, context):
    collectionName = context.user_data['collectionName']
    entryName = update.message.text
    
    if entryName=='Cancel':
        update.message.reply_text("quitting!")
        return
    
    if context.user_data['addremove']=="add":
        if addToCategory(collectionName,entryName)==True:
            update.message.reply_text(str(entryName) +" was successfully added!")
        else:
            update.message.reply_text(str(entryName) +" was not added!")
    elif context.user_data['addremove']=="remove":
        if removeFromCategory(collectionName,entryName)==False:
            update.message.reply_text(str(entryName) +" was successfully removed!")
        else:
            update.message.reply_text(str(entryName) +" was not removed!")
    
    dispatcher.remove_handler(allMessageHandler)
    context.refresh_data()
    return 

############################ Keyboards #########################################
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Edit Preferences', callback_data='preferences')],
              [InlineKeyboardButton('View Scraped Postings', callback_data='scrapedpostings')],
              [InlineKeyboardButton('View Bot Details', callback_data='botdetails')]]
    return InlineKeyboardMarkup(keyboard)

#PREFERENCES
def preferences_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Company', callback_data='addremoveCompany')],
              [InlineKeyboardButton('Title', callback_data='addremoveTitle')],
                [InlineKeyboardButton('Period', callback_data='addremovePeriod')],
                [InlineKeyboardButton('Job Type', callback_data='addremoveJobType')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

def addremoveCompany_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Add', callback_data='addcompany')],
                [InlineKeyboardButton('Remove', callback_data='removecompany')],
                [InlineKeyboardButton('Go back', callback_data='preferences')]]
    return InlineKeyboardMarkup(keyboard)

def addremoveTitle_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Add', callback_data='addtitle')],
                [InlineKeyboardButton('Remove', callback_data='removetitle')],
                [InlineKeyboardButton('Go back', callback_data='preferences')]]
    return InlineKeyboardMarkup(keyboard)

def addremovePeriod_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Add', callback_data='addperiod')],
                [InlineKeyboardButton('Remove', callback_data='removeperiod')],
                [InlineKeyboardButton('Go back', callback_data='preferences')]]
    return InlineKeyboardMarkup(keyboard)

def addremoveJobType_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Add', callback_data='addjobtype')],
                [InlineKeyboardButton('Remove', callback_data='removejobtype')],
                [InlineKeyboardButton('Go back', callback_data='preferences')]]
    return InlineKeyboardMarkup(keyboard)

############################# MESSAGES #########################################
def main_menu_message():
    return 'Select option:'

def preferences_menu_message():
    return 'Select Category:'

def addremove_menu_message():
    return 'Add/Remove Keywords:'

def add_menu_message():
    return 'Add Keywords:\nType out the keyword you would like to add, or \'Cancel\' to quit:'

def remove_menu_message():
    return 'Remove Keywords:\nType out the keyword you would like to remove, or \'Cancel\' to quit:'

def scrapedpostings_message():
    return 'These are the scraped postings from the last 3 days:'

def botdetails_message():
    return 'Bot scrapes the IT categories of InternSG and filters out jobs according to preferences.\nDone at 7am daily'

############################# HANDLERS #########################################
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))


#PREFERENCES
dispatcher.add_handler(CallbackQueryHandler(preferences_menu, pattern='preferences'))
#addremove menus
dispatcher.add_handler(CallbackQueryHandler(addremoveCompany_menu, pattern='addremoveCompany'))
dispatcher.add_handler(CallbackQueryHandler(addremoveTitle_menu, pattern='addremoveTitle'))
dispatcher.add_handler(CallbackQueryHandler(addremovePeriod_menu, pattern='addremovePeriod'))
dispatcher.add_handler(CallbackQueryHandler(addremoveJobType_menu, pattern='addremoveJobType'))
#company,title,period,jobtype
dispatcher.add_handler(CallbackQueryHandler(addcompany_ftn, pattern='addcompany'))
dispatcher.add_handler(CallbackQueryHandler(removecompany_ftn, pattern='removecompany'))
dispatcher.add_handler(CallbackQueryHandler(addtitle_ftn, pattern='addtitle'))
dispatcher.add_handler(CallbackQueryHandler(removetitle_ftn, pattern='removetitle'))
dispatcher.add_handler(CallbackQueryHandler(addperiod_ftn, pattern='addperiod'))
dispatcher.add_handler(CallbackQueryHandler(removeperiod_ftn, pattern='removeperiod'))
dispatcher.add_handler(CallbackQueryHandler(addjobtype_ftn, pattern='addjobtype'))
dispatcher.add_handler(CallbackQueryHandler(removejobtype_ftn, pattern='removejobtype'))

allMessageHandler = MessageHandler(Filters.all,addremove_input)

#SCRAPED POSTINGS, BOT DETAILS
dispatcher.add_handler(CallbackQueryHandler(scrapedpostings_menu, pattern='scrapedpostings'))
dispatcher.add_handler(CallbackQueryHandler(botdetails_menu, pattern='botdetails'))

dispatcher.add_error_handler(error)

updater.start_polling()
################################################################################
