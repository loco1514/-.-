using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Sqlite;
using Microsoft.EntityFrameworkCore.Design;

namespace MeetingRoomBooking
{
    public class Program
    {
        public static void Main(string[] args)
        {
            WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

            // Add services to the container.
            builder.Services.AddControllers();
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();

            //builder.Services.AddDbContext<MeetingRoomBookingContext>(options => options.UseSqlite("Name=ContextDb"));
            builder.Services.AddDbContext<MeetingRoomBookingContext>(options =>
    options.UseSqlite("Data Source=MeetingRoomBooking.db"));

           /* var dbContext = .Services.GetRequiredService<MeetingRoomBookingContext>();
            CreateDBObjects createDBObjects = new CreateDBObjects(dbContext);
            createDBObjects.AddUsersToDatabase();*/

            var app = builder.Build();

            app.UseCors(policy => policy
                .AllowAnyOrigin()
                .AllowAnyHeader()
                .AllowAnyMethod()
            );


            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI();
            }

            app.UseHttpsRedirection();

            app.UseAuthorization();


            app.MapControllers();

            app.Run();
        }
    }
}