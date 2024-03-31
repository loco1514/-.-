namespace MeetingRoomBooking.DTO
{
    public class BookingDTO
    {
        public int UserId { get; set; } 
        public string Data { get; set; }
        public string StartTime { get; set; } 
        public string EndTime { get; set; }
        public int MeetingRoomId { get; set; } 
        public bool Canceled { get; set; } 
        public bool AdmReserve { get; set; }
        public string Description { get; set; }
    }
}
