using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace MeetingRoomBooking.Entities
{
    public class ReportType
    {
        [Key]
        public int Id { get; set; }

        public string ReportText { get; set; }
    }
}
