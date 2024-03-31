using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace MeetingRoomBooking.Entities

{
    public class Report
    {
        [Key]
        public int Id { get; set; }

        [ForeignKey("SenderUser")]
        public int SenderUserId { get; set; }
        public User SenderUser { get; set; }

        [ForeignKey("RecipientUser")]
        public int RecipientUserId { get; set; }
        public User RecipientUser { get; set; }

        [ForeignKey("Booking")]
        public int BookingId { get; set; }
        public Booking Booking { get; set; }

        [ForeignKey("ReportType")]
        public int ReportTypeId { get; set; }
        public ReportType ReportType { get; set; }
        [Required]

        public string Description { get; set; }

    }
}
