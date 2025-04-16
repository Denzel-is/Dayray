using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Migrations;

[Table("log")]
public partial class Log
{
    [Key]
    [Column("login_id")]
    public int LoginId { get; set; }

    [Column("customer_id")]
    public int CustomerId { get; set; }

    [Column("login_time", TypeName = "timestamp without time zone")]
    public DateTime? LoginTime { get; set; }

    [Column("success")]
    public bool Success { get; set; }

    [ForeignKey("CustomerId")]
    [InverseProperty("Logs")]
    public virtual Customer Customer { get; set; } = null!;
}
