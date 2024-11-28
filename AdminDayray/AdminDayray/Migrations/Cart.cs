using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Migrations;

[Table("cart")]
public partial class Cart
{
    [Key]
    [Column("cart_id")]
    public int CartId { get; set; }

    [Column("link_c")]
    [StringLength(100)]
    public string? LinkC { get; set; }

    [Column("product_id")]
    public int? ProductId { get; set; }

    [Column("customer_id")]
    public int? CustomerId { get; set; }

    [Column("quantity")]
    public int? Quantity { get; set; }

    [ForeignKey("CustomerId")]
    [InverseProperty("Carts")]
    public virtual Reg? Customer { get; set; }

    [ForeignKey("ProductId")]
    [InverseProperty("Carts")]
    public virtual Product? Product { get; set; }
}
