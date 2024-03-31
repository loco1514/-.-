using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace MeetingRoomBooking.Entities
{
    public class MeetingRoom
    {
        [Key]
        public int Id { get; set; }

        public int Floor { get; set; }

        public int MeetingRoomId { get; set; }
        [Required]

        public string Description { get; set; }

    }
}
