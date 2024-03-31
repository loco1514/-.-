using MeetingRoomBooking.Entities;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;


namespace MeetingRoomBooking.Controllers
{
    [ApiController]
    [Route("api/meetingRoomBooking")]
    public class MeetingRoomBookingUserController : ControllerBase
    {
        private readonly MeetingRoomBookingContext _context;

        public MeetingRoomBookingUserController(MeetingRoomBookingContext context)
        {
            _context = context;
        }

        [HttpGet("GetUsers")]
        public async Task<ActionResult<List<User>>> GetUsers()
        {
            var users = await _context.Users.ToListAsync();
            return users;
            //return Ok(users);
        }

        // POST api/MeetingRoomUser/CreateUser
        [HttpPost("CreateUser")]
        public async Task<ActionResult<User>> CreateUser(long telegramId, string login)
        {
            var existingUser = await _context.Users.FirstOrDefaultAsync(u => u.TelegramId == telegramId);
            if (existingUser != null)
            {
                return Conflict("User already registered");
            }

            User newUser = new User
            {
                TelegramId = telegramId,
                Login = login
            };

            /*if (email != null)
            {
                newUser.Email = email;
            }
            if (phoneNumber != null)
            {
                newUser.PhoneNumber = phoneNumber;
            }*/

            _context.Users.Add(newUser);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetUserById), new { telegramId = newUser.TelegramId }, newUser);
        }

        // GET api/MeetingRoomUser/{telegramId}
        [HttpGet("GetUserById/{telegramId}")]
        public async Task<ActionResult<User>> GetUserById(long telegramId)
        {
            var user = await _context.Users.FirstOrDefaultAsync(u => u.TelegramId == telegramId);
            if (user == null)
            {
                return NotFound("User not found");
            }

            return user;
        }

    }
}