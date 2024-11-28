using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Migrations;

[Table("employee_schedule")]
public partial class EmployeeSchedule
{
    [Key]
    [Column("schedule_id")]
    public int ScheduleId { get; set; }

    [Column("employee_id")]
    public int? EmployeeId { get; set; }

    [Column("day_of_week")]
    [StringLength(20)]
    public string DayOfWeek { get; set; } = null!;

    [Column("start_time")]
    public TimeOnly? StartTime { get; set; }

    [Column("end_time")]
    public TimeOnly? EndTime { get; set; }

    [ForeignKey("EmployeeId")]
    [InverseProperty("EmployeeSchedules")]
    public virtual Employee? Employee { get; set; }
}
