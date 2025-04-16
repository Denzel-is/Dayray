using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Migrations;

[Table("suppliers")]
public partial class Supplier
{
    [Key]
    [Column("supplier_id")]
    public int SupplierId { get; set; }

    [Column("supplier_name")]
    [StringLength(100)]
    public string SupplierName { get; set; } = null!;

    [Column("contact_person")]
    [StringLength(50)]
    public string? ContactPerson { get; set; }

    [Column("phone_number")]
    [StringLength(20)]
    public string? PhoneNumber { get; set; }

    [Column("email")]
    [StringLength(100)]
    public string? Email { get; set; }

    [InverseProperty("Supplier")]
    public virtual ICollection<ProductSupplier> ProductSuppliers { get; set; } = new List<ProductSupplier>();
}
