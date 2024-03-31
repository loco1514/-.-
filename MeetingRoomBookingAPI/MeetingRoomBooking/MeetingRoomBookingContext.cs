
using MeetingRoomBooking.Entities;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Reflection.Emit;
using System.Threading.Tasks;

namespace MeetingRoomBooking
{
    public class MeetingRoomBookingContext : DbContext
    {
        public DbSet<User> Users { get; set; }
        public DbSet<Booking> Bookings { get; set; }
        public DbSet<MeetingRoom> MeetingRooms { get; set; }
        public DbSet<NotificationService> NotificationServices { get; set; }
        public DbSet<Report> Reports { get; set; }
        public DbSet<ReportType> ReportTypes { get; set; }

        public MeetingRoomBookingContext()
        {
            //Database.EnsureCreated();
        }

        public MeetingRoomBookingContext(DbContextOptions<MeetingRoomBookingContext> options)
            : base(options)
        {
        }

        // Метод OnModelCreating для настройки моделей и данных
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<ReportType>().HasData(
                new ReportType { Id = 1, ReportText = "Превышение времени бронирования" },
                new ReportType { Id = 2, ReportText = "Неявка по бронированию" },
                new ReportType { Id = 3, ReportText = "Использование комнаты не по цели" },
                new ReportType { Id = 4, ReportText = "Оставил личные вещи" },
                new ReportType { Id = 5, ReportText = "Оставил беспорядок" },
                new ReportType { Id = 6, ReportText = "Спит" }
            );

            // Другие настройки моделей

            base.OnModelCreating(modelBuilder);
        }

    }
}
