using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Migrations;

[Table("transactions")]
public partial class Transaction
{
    [Key]
    [Column("transaction_id")]
    public int TransactionId { get; set; }

    [Column("order_id")]
    public int? OrderId { get; set; }

    [Column("transaction_date", TypeName = "timestamp without time zone")]
    public DateTime? TransactionDate { get; set; }

    [Column("payment_method")]
    [StringLength(50)]
    public string? PaymentMethod { get; set; }

    [Column("amount_paid")]
    [Precision(10, 2)]
    public decimal? AmountPaid { get; set; }

    [Column("payment_method_id")]
    public int? PaymentMethodId { get; set; }

    [ForeignKey("OrderId")]
    [InverseProperty("Transactions")]
    public virtual Order? Order { get; set; }

    [ForeignKey("PaymentMethodId")]
    [InverseProperty("Transactions")]
    public virtual PaymentMethod? PaymentMethodNavigation { get; set; }
}
