using MeetingRoomBooking.Entities;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;


namespace MeetingRoomBooking.Controllers
{
    [ApiController]
    [Route("api/meetingRoomBooking")]
    public class MeetingRoomBookingADMController : ControllerBase
    {
        private readonly MeetingRoomBookingContext _context;
        private const string MESSAGEFORACCEPTADMINSTATUS = "/addADM";

        public MeetingRoomBookingADMController(MeetingRoomBookingContext context)
        {
            _context = context;
        }

        [HttpGet("GetReports")]
        public async Task<ActionResult<List<Report>>> GetReports()
        {
            var reports = await _context.Reports
                .Include(b => b.SenderUser)
                .Include(b => b.RecipientUser)
                .Include(b => b.ReportType)
                .Include(b => b.Booking)
                .ToListAsync();

            return reports;
            //return Ok(reports);
        }

        [HttpPut("Update")]
        public async Task<ActionResult<bool>> UpdateUserAccess([FromBody] User updatedUser, string message)
        {
            if (updatedUser == null)
            {
                return BadRequest("Incorrect data");
            }

            if (message.Contains(MESSAGEFORACCEPTADMINSTATUS))
            {
                updatedUser.Admin = true;
                _context.Users.Update(updatedUser);
                await _context.SaveChangesAsync();
                return Ok(true);
            }
            else
            {
                return BadRequest("Incorrect message for updating status");
            }
        }

        public class ReservationRequest
        {
            public DateTime TimeFrom { get; set; }
            public DateTime TimeTo { get; set; }
            public List<MeetingRoom> MeetingRooms { get; set; }
        }

        [HttpPost("ReserveForPeriod")]
        public async Task<ActionResult<bool>> ReserveForPeriod([FromBody] ReservationRequest request)
        {
            DateTime currentDate = DateTime.Now.Date;

            if (request.TimeFrom >= currentDate && request.TimeTo >= currentDate)
            {
                return false;
            }

            return true;
        }
    }
}
