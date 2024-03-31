using MeetingRoomBooking.Entities;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MeetingRoomBooking.DTO;

namespace MeetingRoomBooking.Controllers
{
    [ApiController]
    [Route("api/meetingRoomBooking")]
    public class MeetingRoomBookingBookingController : ControllerBase
    {
        private readonly MeetingRoomBookingContext _context;
        //private const string MESSAGEFORACCEPTADMINSTATUS = "/addADM";

        public MeetingRoomBookingBookingController(MeetingRoomBookingContext context)
        {
            _context = context;
        }

        // POST api/MeetingRoomUser/CreateBooking
        [HttpPost("CreateBooking")]
        public async Task<ActionResult<Booking>> CreateBooking(BookingDTO bookingDTO)
        {
            if (bookingDTO == null)
            {
                return BadRequest("Booking data is null.");
            }

            var user = await _context.Users.FindAsync(bookingDTO.UserId);
            if (user == null)
            {
                return NotFound("User not found.");
            }

            var meetingRoom = await _context.MeetingRooms.FindAsync(bookingDTO.MeetingRoomId);
            if (meetingRoom == null)
            {
                return NotFound("Meeting room not found.");
            }

            var newBooking = new Booking
            {
                UserId = bookingDTO.UserId,
                Data = bookingDTO.Data,
                StartTime = bookingDTO.StartTime,
                EndTime = bookingDTO.EndTime,
                MeetingRoomId = bookingDTO.MeetingRoomId,
                Canceled = bookingDTO.Canceled,
                AdmReserve = bookingDTO.AdmReserve,
                Description = bookingDTO.Description
            };

            _context.Bookings.Add(newBooking);
            await _context.SaveChangesAsync();

            return Ok(newBooking);
        }

      /*      return CreatedAtAction(nameof(GetUserById), new { telegramId = newUser.TelegramId }, newUser);
        }
*/
        [HttpGet("GetBookings")]
        public async Task<ActionResult<List<Booking>>> GetBookings()
        {
            var bookings = await _context.Bookings.ToListAsync();
            return bookings;
            //return Ok(bookings);
        }

        [HttpGet("GetBookingsByFloor")]
        public async Task<ActionResult<List<Booking>>> GetBookingsByFloor(int floor)
        {
            var bookingsByFloor = await _context.Bookings
                .Include(b => b.MeetingRoom)
                .Where(b => b.MeetingRoom.Floor == floor)
                .ToListAsync();

            if (bookingsByFloor.Count == 0)
            {
                return NotFound("No bookings found for the specified floor");
            }

            return bookingsByFloor;
        }

        [HttpGet("GetBookingsByMeetingRoomId")]
        public async Task<ActionResult<List<Booking>>> GetBookingsByMeetingRoomId(int meetingRoomId)
        {
            var bookingsByMeetingRoomId = await _context.Bookings
                .Include(b => b.MeetingRoom)
                .Where(b => b.MeetingRoom.MeetingRoomId == meetingRoomId)
                .ToListAsync();

            if (bookingsByMeetingRoomId.Count == 0)
            {
                return NotFound("No bookings found for the specified meeting room");
            }

            return bookingsByMeetingRoomId;
        }

        [HttpGet("GetBookingsByUserId")]
        public async Task<ActionResult<List<Booking>>> GetBookingsByUserId(long userId)
        {
            var bookingsByUserId = await _context.Bookings
                .Include(b => b.User)
                .Include(b => b.MeetingRoom)
                .Where(b => b.User.TelegramId == userId)
                .ToListAsync();

            if (bookingsByUserId.Count == 0)
            {
                return NotFound("No bookings found for the specified user");
            }

            return bookingsByUserId;
        }

        [HttpGet("GetBookingsByData")]
        public async Task<ActionResult<List<Booking>>> GetBookingsByData(string data)
        {
            var bookingsByData = await _context.Bookings
                .Include(b => b.User)
                .Include(b => b.MeetingRoom)
                .Where(b => b.Data == data)
                .ToListAsync();

            if (bookingsByData.Count == 0)
            {
                return NotFound("No bookings found for the specified user");
            }

            return bookingsByData;
        }

        [HttpPut("CanceleBooking")]
        public async Task<ActionResult> CanceleBooking(int bookingId)
        {
            var bookingToDelete = await _context.Bookings.FindAsync(bookingId);

            if (bookingToDelete == null)
            {
                return NotFound("Booking not found");
            }

            bookingToDelete.Canceled = true;
            _context.Update(bookingToDelete);
            await _context.SaveChangesAsync();

            return Ok("Booking canceled");
        }
    }
}
