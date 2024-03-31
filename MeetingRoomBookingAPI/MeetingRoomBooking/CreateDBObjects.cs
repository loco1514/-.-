using MeetingRoomBooking.Entities;

namespace MeetingRoomBooking
{
    public class CreateDBObjects
    {
        private readonly MeetingRoomBookingContext _context;

        public CreateDBObjects(MeetingRoomBookingContext context)
        {
            _context = context;
        }

        public CreateDBObjects()
        {

        }

        public void AddUsersToDatabase()
        {
            Random random = new Random();

            for (int i = 0; i < 5; i++)
            {
                var newUser = new User
                {
                    TelegramId = random.Next(1000000, 9999999), // Генерация случайного TelegramId
                    Login = $"user{i + 1}", // Генерация логина вида "user1", "user2", и т.д.
                    //Email = $"user{i + 1}@example.com", // Генерация адреса электронной почты
                    //PhoneNumber = "+1234567890", // Пример номера телефона
                };

                if (i == 0)
                {
                    newUser.Admin = true;
                    newUser.Login = "admin";
                }

                _context.Users.Add(newUser); // Добавляем пользователя в контекст
            }

            _context.SaveChanges(); // Сохраняем изменения в базе данных
        }

        public void AddMeetingRoomsToDatabase()
        {
            Random random = new Random();

            for (int i = 0; i < 5; i++)
            {
                var newMeetingRoom = new MeetingRoom
                {
                    Floor = random.Next(17, 20), // Генерация случайного этажа
                    MeetingRoomId = i + 1, // Просто увеличиваем ID для примера
                    Description = $"Meeting room {i + 1}" // Генерация описания
                };

                _context.MeetingRooms.Add(newMeetingRoom); // Добавляем комнату в контекст
            }

            _context.SaveChanges(); // Сохраняем изменения в базе данных
        }

        public void AddBookingsToDatabase()
        {
            Random random = new Random();

            var users = _context.Users.ToList();
            var meetingRooms = _context.MeetingRooms.ToList();

            for (int i = 0; i < 10; i++)
            {
                var newUser = users[random.Next(users.Count)];
                var newMeetingRoom = meetingRooms[random.Next(meetingRooms.Count)];

                var newBooking = new Booking
                {
                    UserId = newUser.Id, // Выбираем случайного пользователя из списка
                    Data = DateTime.Now.Date.AddDays(random.Next(1, 10)).ToString("dd.MM.yyyy"), // Генерация случайной даты в ближайшие 10 дней
                    StartTime = DateTime.Now.Date.AddHours(random.Next(8, 16)).ToString("HH:mm"), // Генерация случайного времени начала бронирования
                    EndTime = DateTime.Now.Date.AddHours(random.Next(16, 23)).ToString("HH:mm"), // Генерация случайного времени окончания бронирования
                    MeetingRoomId = newMeetingRoom.Id, // Выбираем случайную комнату из списка
                    MeetingRoom = newMeetingRoom,
                    Description = $"Booking {i + 1}" // Генерация описания
                };

                _context.Bookings.Add(newBooking); // Добавляем бронирование в контекст
            }

            _context.SaveChanges(); // Сохраняем изменения в базе данных
        }

        public void AddNotificationsToDatabase()
        {
            Random random = new Random();

            var bookings = _context.Bookings.ToList();

            for (int i = 0; i < 7; i++)
            {
                var randomBooking = bookings[random.Next(bookings.Count)];

                var newNotification = new NotificationService
                {
                    BookingId = randomBooking.Id, // Выбираем случайное бронирование из списка
                    Booking = randomBooking,
                    NotifiedStart = false, // Генерация случайного значения для NotifiedStart
                    NotifiedStop = false // Генерация случайного значения для NotifiedStop
                };

                _context.NotificationServices.Add(newNotification); // Добавляем запись в контекст
            }

            _context.SaveChanges(); // Сохраняем изменения в базе данных
        }


        public void AddReportsToDatabase()
        {
            Random random = new Random();

            var users = _context.Users.ToList();
            var bookings = _context.Bookings.ToList();
            var reportTypes = _context.ReportTypes.ToList();

            for (int i = 0; i < 7; i++)
            {
                User randomSenderUser = users[random.Next(users.Count)];
                User randomRecipientUser = users[random.Next(users.Count)];
                Booking randomBooking = bookings[random.Next(bookings.Count)];
                ReportType randomReportType = reportTypes[random.Next(reportTypes.Count)];

                var newReport = new Report
                {
                    SenderUserId = randomSenderUser.Id, // Выбираем случайного отправителя из списка
                    RecipientUserId = randomRecipientUser.Id, // Выбираем случайного получателя из списка
                    BookingId = randomBooking.Id, // Выбираем случайное бронирование из списка
                    ReportTypeId = randomReportType.Id, // Выбираем случайный тип отчета из списка
                    ReportType = randomReportType,
                    Booking= randomBooking,
                    RecipientUser = randomRecipientUser,
                    SenderUser= randomSenderUser,
                    Description = $"Report {i + 1}" // Генерация описания
                };

                _context.Reports.Add(newReport); // Добавляем запись в контекст
            }

            _context.SaveChanges(); // Сохраняем изменения в базе данных
        }
    }
}
