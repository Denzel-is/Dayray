using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Migrations;

[PrimaryKey("ProductId", "SupplierId")]
[Table("product_suppliers")]
public partial class ProductSupplier
{
    [Key]
    [Column("product_id")]
    public int ProductId { get; set; }

    [Key]
    [Column("supplier_id")]
    public int SupplierId { get; set; }

    [Column("unit_price")]
    [Precision(8, 2)]
    public decimal? UnitPrice { get; set; }

    [ForeignKey("ProductId")]
    [InverseProperty("ProductSuppliers")]
    public virtual Product Product { get; set; } = null!;

    [ForeignKey("SupplierId")]
    [InverseProperty("ProductSuppliers")]
    public virtual Supplier Supplier { get; set; } = null!;
}
