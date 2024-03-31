using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace MeetingRoomBooking.Entities

{
    public class Booking
    {
        [Key]
        public int Id { get; set; }

        [ForeignKey("User")]
        public int UserId { get; set; }
        public User User { get; set; }

        public string Data { get; set; } 

        public string StartTime { get; set; }

        public string EndTime { get; set; }

        [ForeignKey("MeetingRoom")]
        public int MeetingRoomId { get; set; }
        public MeetingRoom MeetingRoom { get; set; }

        //public DateTime PlannedTime { get; set; }
        public bool Canceled { get; set; } = false;

        public bool AdmReserve { get; set; } = false;
        public string Description { get; set; }

    }
}
