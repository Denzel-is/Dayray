using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Migrations;

[Table("payment_methods")]
public partial class PaymentMethod
{
    [Key]
    [Column("payment_method_id")]
    public int PaymentMethodId { get; set; }

    [Column("customer_id")]
    public int? CustomerId { get; set; }

    [Column("card_holder_name")]
    [StringLength(100)]
    public string? CardHolderName { get; set; }

    [Column("card_number")]
    [StringLength(16)]
    public string? CardNumber { get; set; }

    [Column("card_expiry_date")]
    public DateOnly? CardExpiryDate { get; set; }

    [Column("card_cvv")]
    [StringLength(4)]
    public string? CardCvv { get; set; }

    [Column("address")]
    public string? Address { get; set; }

    [ForeignKey("CustomerId")]
    [InverseProperty("PaymentMethods")]
    public virtual Reg? Customer { get; set; }

    [InverseProperty("PaymentMethodNavigation")]
    public virtual ICollection<Transaction> Transactions { get; set; } = new List<Transaction>();
}
