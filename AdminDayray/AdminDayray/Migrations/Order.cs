using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Migrations;

[Table("orders")]
public partial class Order
{
    [Key]
    [Column("order_id")]
    public int OrderId { get; set; }

    [Column("customer_id")]
    public int? CustomerId { get; set; }

    [Column("order_date", TypeName = "timestamp without time zone")]
    public DateTime? OrderDate { get; set; }

    [Column("total_amount")]
    [Precision(10, 2)]
    public decimal? TotalAmount { get; set; }

    [Column("status")]
    [StringLength(20)]
    public string? Status { get; set; }

    [ForeignKey("CustomerId")]
    [InverseProperty("Orders")]
    public virtual Reg? Customer { get; set; }

    [InverseProperty("Order")]
    public virtual ICollection<OrderItem> OrderItems { get; set; } = new List<OrderItem>();

    [InverseProperty("Order")]
    public virtual ICollection<Transaction> Transactions { get; set; } = new List<Transaction>();
}
