using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Migrations;

[Table("feedback")]
public partial class Feedback
{
    [Key]
    [Column("feedback_id")]
    public int FeedbackId { get; set; }

    [Column("customer_id")]
    public int? CustomerId { get; set; }

    [Column("feedback_text")]
    public string? FeedbackText { get; set; }

    [Column("cust_name")]
    [StringLength(100)]
    public string? CustName { get; set; }

    [Column("feedback_date")]
    public DateOnly? FeedbackDate { get; set; }

    [ForeignKey("CustomerId")]
    [InverseProperty("Feedbacks")]
    public virtual Reg? Customer { get; set; }
}
