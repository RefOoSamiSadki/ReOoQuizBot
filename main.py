import telebot
import pdfplumber
from io import BytesIO
from get_questions import get_questions
from keep_alive import keep_alive
import time
class QuizBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.TOPIC = None
        self.NUM_QUESTIONS = None
        self.DIFF = None


    def start(self):
        @self.bot.callback_query_handler(func=lambda call: call.data == "help")
        def send_help_message(call):
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton("تواصل📞", url="https://t.me/RefOoSami"))
            help_text = (
                "*مرحبًا بك في مركز المساعدة !* 🤖📚\n\n"
                "الأوامر المتاحة:\n"
                "/start - لبدء استخدام البوت وعرض الخيارات.\n"
                "/addpremium - لإضافة مستخدمين إلى الخطة المدفوعة، لميزات إضافية (للمشرفين).\n"
                "/removepremium - لإزالة مستخدمين من الخطة المدفوعة (للمشرفين).\n\n"
                "*لإنشاء اختبار، اتبع الخطوات دي:*\n"
                "1. ابعت محتوى المحاضرة كنص أو ملف PDF أو صورة.\n"
                "2. اختار عدد الأسئلة اللي عايزها في الاختبار.\n"
                "3. حدد مستوى الصعوبة (سهل، متوسط، أو صعب).\n"
                "4. استنى لحد ما البوت يخلص إنشاء الأسئلة على حسب اختيارك.\n\n"
                "*ملاحظة:*\n"
                "- تأكد إن المحتوى اللي بتبعتوه متعلق بموضوع معين علشان جودة الأسئلة تبقى عالية.\n"
                "- يفضل تراجع الأسئلة قبل استخدامها في الاختبار، علشان تتأكد إنها دقيقة.\n"
                "- لو عندك أي استفسارات أو محتاج مساعدة، تواصل معانا! 😊\n"
            )

            self.bot.send_message(call.message.chat.id, help_text, reply_markup=markup,parse_mode="Markdown")

                
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.send_user_details(854578633, message.from_user)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row_width = 2

            # Add "إنشاء اختبار" button in one row
            markup.add(telebot.types.InlineKeyboardButton("إنشاء اختبار🧠", callback_data="start_quiz"))

            # Create a new row and add the other two buttons
            new_row = []
            new_row.append(telebot.types.InlineKeyboardButton("تواصل📞", url="https://t.me/RefOoSami"))
            new_row.append(telebot.types.InlineKeyboardButton("مساعدة🤝", callback_data="help"))
            markup.add(*new_row)

            disclaimer_message = (
                "خد بالك إن الأسئلة اللي البوت بيولدها ممكن يكون فيها أخطاء. البوت ده بيساعدك في إعداد الأسئلة، "
                "مش عشان تولد الاختبارات بالكامل. ياريت تراجع الأسئلة بنفسك.🚫"
            )

            self.bot.send_message(
                message.chat.id,
                f"أهلاً👋\nللبدء اضغط على *إنشاء اختبار🧠*\n\n{disclaimer_message}",
                reply_markup=markup,
                parse_mode='Markdown'
            )


        @self.bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
        def start_quiz(call):
            chat_id = call.message.chat.id
            message = """
                *مرحبًا👋\n\n إزاي تفضل تبعت المادة العلمية؟ 🤔*
            """

            markup = telebot.types.InlineKeyboardMarkup()
            markup.row_width = 1
            markup.add(telebot.types.InlineKeyboardButton("نص📝", callback_data="text_lecture"),
                        telebot.types.InlineKeyboardButton("🗃️PDF", callback_data="pdf_lecture"))
            self.bot.delete_message(chat_id, call.message.message_id)
            self.bot.send_message(chat_id, message, reply_markup=markup,parse_mode='Markdown')

        @self.bot.callback_query_handler(func=lambda call: call.data == "text_lecture")
        def send_lecture_as_text(call):
            chat_id = call.message.chat.id
            self.bot.delete_message(chat_id, call.message.message_id)
            self.bot.send_message(chat_id, "برجاء ارسال محتوى المحاضرة في رسالة📝\n*يجب ارسال مادة علمية وليس عنوان لموضوع!*", parse_mode='Markdown')
            self.bot.register_next_step_handler(call.message, self.get_topic_from_text)

        @self.bot.callback_query_handler(func=lambda call: call.data == "pdf_lecture")
        def send_lecture_as_pdf(call):
            chat_id = call.message.chat.id
            self.bot.delete_message(chat_id, call.message.message_id)
            self.bot.send_message(chat_id, "برجاء ارسال ملف PDF🗃️\nلازم يكون الملف PDF مش صور محولة لـ PDF.")
            self.bot.register_next_step_handler(call.message, self.get_topic_from_pdf)
            

        @self.bot.callback_query_handler(func=lambda call: call.data in ["5", "10", "20", "40", "60", "80"])
        def select_num_questions(call):
            self.NUM_QUESTIONS = call.data
            self.get_difficulty_level(call.message)

        @self.bot.callback_query_handler(func=lambda call: call.data in ["easy", "medium", "hard",'mixed'])
        def select_difficulty_level(call):
            self.DIFF = call.data
            self.create_quiz(call.message)
            
        @self.bot.callback_query_handler(func=lambda call: call.data in ["feedback_yes", "feedback_no"])
        def handle_feedback(call):
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            chat_id = call.message.chat.id
            if call.data == "feedback_yes":
                self.bot.send_message(chat_id, "متشكرين جداً على التقييم! 🌟")
                self.bot.send_sticker(chat_id, "CAACAgIAAxkBAAIVemYUNaMv-VaGZU18xrZTh-_z3xTIAAIEAQACVp29Ct4E0XpmZvdsNAQ")
                self.bot.send_message(854578633, f"المستخدم {chat_id} قيم البوت بانه جيد")
            elif call.data == "feedback_no":
                # Send a contact button for the user to contact support
                contact_button = telebot.types.InlineKeyboardMarkup()
                contact_button.add(telebot.types.InlineKeyboardButton("تواصل بالدعم💁", url="https://t.me/RefOoSami"))

                self.bot.send_message(
                    chat_id,
                    "احنا آسفين إنك مش مبسوط. لو عندك أي ملاحظات أو اقتراحات، متترددش تشاركها معانا. 🙏",
                    reply_markup=contact_button
                )
                self.bot.send_sticker(chat_id, "CAACAgIAAxkBAAIVfGYUNnYBOTnkuw982--5-LHV74ItAALzAANWnb0KahvrxMf6lv40BA")
                self.bot.send_message(854578633, f"المستخدم {chat_id} قيم البوت بانه غير مقبول")
        self.bot.polling()

    def get_topic_from_text(self, message):
        if message.text is None:
            self.bot.send_message(message.chat.id, "مفيش نص مدخل. برجاء إدخال نص الموضوع.")
            self.bot.register_next_step_handler(message, self.get_topic_from_text)
            return

        if len(message.text) < 60:  # Adjust the threshold as needed
            self.bot.send_message(message.chat.id, "المحتوى اللي كتبته قصير جدًا. برجاء إدخال محتوى أطول.")
            self.bot.register_next_step_handler(message, self.get_topic_from_text)
            return

        self.TOPIC = message.text
        self.get_num_questions(message)


    def get_topic_from_pdf(self, message):
        if message.document:
            if message.document.mime_type == 'application/pdf':
                initial_reply = self.bot.reply_to(message, 'جاري استخراج البيانات، استنى شوية⌛')
                file_info = self.bot.get_file(message.document.file_id)
                downloaded_file = self.bot.download_file(file_info.file_path)
                with pdfplumber.open(BytesIO(downloaded_file)) as pdf:
                    page_count = len(pdf.pages)
                    self.bot.delete_message(message.chat.id, initial_reply.message_id)
                    get_num_msg = (f"تم استخراج *{page_count}* صفحة من الملف. الترقيم بالنسبة لينا بيبدأ من الصفحة الأولى بغض النظر عن ترقيم الصفحات في الملف"
                                "\n*يرجى تحديد الصفحات المطلوبة، مثال: 17-13. *")
                    self.bot.reply_to(message, get_num_msg,parse_mode='Markdown')
                    self.bot.register_next_step_handler(message, lambda msg: self.extract_text_from_pages(msg, pdf))
            else:
                self.bot.reply_to(message, "الملف اللي بعته مش PDF. برجاء إرسال ملف PDF.")
                self.bot.register_next_step_handler(message, self.get_topic_from_pdf)
        else:
            self.bot.reply_to(message, "الرجاء إرسال ملف PDF.")
            self.bot.register_next_step_handler(message, self.get_topic_from_pdf)
            
            
    def extract_text_from_pages(self,message, pdf):
        selected_pages = message.text.strip().split(',')
        extracted_text = ''
        invalid_input = False
        try:
            for page_range in selected_pages:
                if '-' in page_range:
                    start, end = map(int, page_range.split('-'))
                    if 1 <= start <= end <= len(pdf.pages):
                        for i in range(start, end + 1):
                            extracted_text += pdf.pages[i - 1].extract_text()
                    else:
                        self.bot.send_message(message.chat.id, f"النطاق {page_range} غير صالح. يرجى تقديم نطاق صحيح.")
                        invalid_input = True
                        break
                else:
                    page_num = int(page_range)
                    if 1 <= page_num <= len(pdf.pages):
                        extracted_text += pdf.pages[page_num - 1].extract_text()
                    else:
                        self.bot.send_message(message.chat.id, f"الصفحة {page_num} غير موجودة في الملف. يرجى تقديم صفحة صالحة.")
                        invalid_input = True
                        break
        except ValueError:
            self.bot.send_message(message.chat.id, f"القيمة '{page_range}' غير صالحة. يرجى اختيار صفحة صالحة.")
            invalid_input = True
        if not invalid_input:
            self.TOPIC = extracted_text
            self.get_num_questions(message)
        else:
            self.bot.register_next_step_handler(message, lambda msg: self.extract_text_from_pages(msg, pdf))
            
    def get_num_questions(self, message):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row_width = 3
        markup.add(telebot.types.InlineKeyboardButton("5️⃣", callback_data="5"),
                   telebot.types.InlineKeyboardButton("🔟", callback_data="10"),
                   telebot.types.InlineKeyboardButton("2️⃣0️⃣", callback_data="20"))
        markup.add(telebot.types.InlineKeyboardButton("4️⃣0️⃣", callback_data="40"),
                   telebot.types.InlineKeyboardButton("6️⃣0️⃣", callback_data="60"),
                   telebot.types.InlineKeyboardButton("8️⃣0️⃣", callback_data="80"))
        # Send the message with the buttons
        sent_message = self.bot.send_message(
            message.chat.id, 
            "*أختار عدد الأسئلة المطلوبة في الاختبار*😌\nممكن عدد الاسئلة يختلف حسب كمية المحتوى وصعوبة الأسئلة", 
            reply_markup=markup, 
            parse_mode='Markdown'
        )

    def get_difficulty_level(self, message):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(
            telebot.types.InlineKeyboardButton("متوسط😌", callback_data="medium"),
            telebot.types.InlineKeyboardButton("سهل💤", callback_data="easy"),
            telebot.types.InlineKeyboardButton("مزيج🤔", callback_data="mixed"),
            telebot.types.InlineKeyboardButton("صعب😓", callback_data="hard"),

        )
        self.bot.delete_message(message.chat.id, message.message_id)
        # Send the message with the buttons
        self.bot.send_message(
            message.chat.id, 
            "اختار مستوى الصعوبة 🏋\nأنصح باختيار *ميكس* لإنشاء أسئلة بمستويات مختلفة🎉", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )



    def get_num_questions(self, message):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row_width = 3
        markup.add(telebot.types.InlineKeyboardButton("5️⃣", callback_data="5"),
                   telebot.types.InlineKeyboardButton("🔟", callback_data="10"),
                   telebot.types.InlineKeyboardButton("2️⃣0️⃣", callback_data="20"))
        markup.add(telebot.types.InlineKeyboardButton("4️⃣0️⃣", callback_data="40"),
                   telebot.types.InlineKeyboardButton("6️⃣0️⃣", callback_data="60"),
                   telebot.types.InlineKeyboardButton("8️⃣0️⃣", callback_data="80"))
        self.bot.send_message(message.chat.id, "أختار عدد الأسئلة المطلوبة في الاختبار", reply_markup=markup)




        
    def create_quiz(self, message):
        self.bot.delete_message(message.chat.id, message.message_id)
        wait_message = self.bot.send_message(
        message.chat.id,"*جارٍ إنشاء الأسئلة* 🫣\n🔹ممكن عدد الأسئلة يختلف حسب المحتوى\n🔹راجع الأسئلة لإنه ممكن يكون فيها نسبة خطأ!\n🔹استنى شوية، ممكن تاخد لحد *5* دقايق...", parse_mode='Markdown')
        loading_animation = self.bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAIU1GYOk5jWvCvtykd7TZkeiFFZRdUYAAIjAAMoD2oUJ1El54wgpAY0BA")
        
        def send_error_message():
            self.bot.delete_message(message.chat.id, wait_message.message_id)
            self.bot.delete_message(message.chat.id, loading_animation.message_id)
            self.bot.send_message(message.chat.id, "حصلت مشكلة أثناء إنشاء الأسئلة. حاول تاني لو سمحت.")
        
        if self.DIFF == "mixed":
            for difficulty in ["easy", "medium", "hard"]:
                num_questions_per_level = int(self.NUM_QUESTIONS) // 3
                parsed_data = get_questions(difficulty, num_questions_per_level, self.TOPIC)
                
                if not isinstance(parsed_data, dict):
                    send_error_message()
                    return
                
                try:
                    self.bot.delete_message(message.chat.id, wait_message.message_id)
                    self.bot.delete_message(message.chat.id, loading_animation.message_id)
                except:
                    pass
                
                diff_levels = {
                    "easy": "سهل",
                    "medium": "متوسط",
                    "hard": "صعب"
                }
                diff_level = diff_levels.get(difficulty)
                self.bot.send_message(message.chat.id, f"أسئلة بمستوى صعوبة *{diff_level}*🎉", parse_mode='Markdown')
                
                for question_number, question_data in parsed_data.items():
                    try:
                        question_text = question_data["text"]
                        options = question_data["options"]
                        correct_answer = question_data["answer"]
                    except KeyError:
                        continue
                    
                    options_list = [f"{key}. {value}" for key, value in options.items()]
                    
                    if any(len(option) > 100 for option in options_list):
                        continue
                    
                    poll_message = self.bot.send_poll(
                        chat_id=message.chat.id,
                        question=question_text,
                        options=options_list,
                        is_anonymous=True,
                        type="quiz",
                        correct_option_id=list(options.keys()).index(correct_answer),
                        open_period=0,
                        protect_content=False
                    )
        else:
            parsed_data = get_questions(self.DIFF, self.NUM_QUESTIONS, self.TOPIC)
            
            if not isinstance(parsed_data, dict):
                send_error_message()
                return
            
            self.bot.delete_message(message.chat.id, wait_message.message_id)
            self.bot.delete_message(message.chat.id, loading_animation.message_id)
            
            try:
                for question_number, question_data in parsed_data.items():
                    try:
                        question_text = question_data["text"]
                        options = question_data["options"]
                        correct_answer = question_data["answer"]
                    except KeyError:
                        continue
                    
                    options_list = [f"{key}. {value}" for key, value in options.items()]
                    
                    if any(len(option) > 100 for option in options_list):
                        continue
                    
                    self.bot.send_poll(
                        chat_id=message.chat.id,
                        question=question_text,
                        options=options_list,
                        is_anonymous=True,
                        type="quiz",
                        correct_option_id=list(options.keys()).index(correct_answer),
                        open_period=0,
                        protect_content=False
                    )
            except:
                pass
        
        self.bot.send_message(message.chat_id, "لو سمحت ممكن تقيم البوت؟ 🌟", reply_markup=self.feedback_options())

    def send_user_details(self, admin_id, user):
        user_details = (
            f"User Details:\n"
            f"Username: {user.username}\n"
            f"Full Name: {user.first_name} {user.last_name}\n"
            f"User ID: {user.id}\n"
            f"Language Code: {user.language_code}\n"
        )
        self.bot.send_message(admin_id, user_details)

    def feedback_options(self):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("👍", callback_data="feedback_yes"),
            telebot.types.InlineKeyboardButton("👎", callback_data="feedback_no")
        )
        return markup

if __name__ == "__main__":
    keep_alive()
    while True:
        try:QuizBot("6982141096:AAFpEspslCkO0KWNbONnmWjUU_87jib__g8").start()
        except:pass
