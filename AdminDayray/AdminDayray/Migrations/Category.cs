using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Migrations;

[Table("categories")]
public partial class Category
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    [Column("category_id")]
    public int CategoryId { get; set; }

    [Column("name")]
    [StringLength(50)]
    public string Name { get; set; } = null!;

    [Column("map")]
    [StringLength(100)]
    public string? Map { get; set; }

    [InverseProperty("Category")]
    public virtual ICollection<Product> Products { get; set; } = new List<Product>();

    [ForeignKey("CategoryId")]
    [InverseProperty("Categories")]
    public virtual ICollection<Product> ProductsNavigation { get; set; } = new List<Product>();
}
