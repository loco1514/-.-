using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace MeetingRoomBooking.Entities

{
    public class NotificationService
    {
        [Key]
        public int Id { get; set; }

        [ForeignKey("Booking")]
        public int BookingId { get; set; }
        public Booking Booking { get; set; }

        public bool NotifiedStart { get; set; } = false;

        public bool NotifiedStop { get; set; } = false;
    }
}
