using System;
using System.Collections.Generic;
using AdminDayray.Migrations;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Context;

public partial class MyDbContext : DbContext
{
    public MyDbContext()
    {
    }

    public MyDbContext(DbContextOptions<MyDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Cart> Carts { get; set; }

    public virtual DbSet<Category> Categories { get; set; }

    public virtual DbSet<Customer> Customers { get; set; }

    public virtual DbSet<Employee> Employees { get; set; }

    public virtual DbSet<EmployeeSchedule> EmployeeSchedules { get; set; }

    public virtual DbSet<Feedback> Feedbacks { get; set; }

    public virtual DbSet<Log> Logs { get; set; }

    public virtual DbSet<Order> Orders { get; set; }

    public virtual DbSet<OrderItem> OrderItems { get; set; }

    public virtual DbSet<PaymentMethod> PaymentMethods { get; set; }

    public virtual DbSet<Product> Products { get; set; }

    public virtual DbSet<ProductSupplier> ProductSuppliers { get; set; }

    public virtual DbSet<Reg> Regs { get; set; }

    public virtual DbSet<Supplier> Suppliers { get; set; }

    public virtual DbSet<Transaction> Transactions { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see https://go.microsoft.com/fwlink/?LinkId=723263.
        => optionsBuilder.UseNpgsql("Host=localhost;Port=5432;Database=Dayray;Username=postgres;Password=food;");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Cart>(entity =>
        {
            entity.HasKey(e => e.CartId).HasName("cart_pkey");

            entity.HasOne(d => d.Customer).WithMany(p => p.Carts).HasConstraintName("cart_customer_id_fkey");

            entity.HasOne(d => d.Product).WithMany(p => p.Carts).HasConstraintName("cart_product_id_fkey");
        });

        modelBuilder.Entity<Category>(entity =>
        {
            entity.HasKey(e => e.CategoryId).HasName("categories_pkey");
        });

        modelBuilder.Entity<Customer>(entity =>
        {
            entity.HasKey(e => e.CustomerId).HasName("customers_pkey");
        });

        modelBuilder.Entity<Employee>(entity =>
        {
            entity.HasKey(e => e.EmployeeId).HasName("employees_pkey");
        });

        modelBuilder.Entity<EmployeeSchedule>(entity =>
        {
            entity.HasKey(e => e.ScheduleId).HasName("employee_schedule_pkey");

            entity.HasOne(d => d.Employee).WithMany(p => p.EmployeeSchedules).HasConstraintName("employee_schedule_employee_id_fkey");
        });

        modelBuilder.Entity<Feedback>(entity =>
        {
            entity.HasKey(e => e.FeedbackId).HasName("feedback_pkey");

            entity.Property(e => e.FeedbackDate).HasDefaultValueSql("now()");

            entity.HasOne(d => d.Customer).WithMany(p => p.Feedbacks).HasConstraintName("feedback_customer_id_fkey");
        });

        modelBuilder.Entity<Log>(entity =>
        {
            entity.HasKey(e => e.LoginId).HasName("log_pkey");

            entity.HasOne(d => d.Customer).WithMany(p => p.Logs)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("log_customer_id_fkey");
        });

        modelBuilder.Entity<Order>(entity =>
        {
            entity.HasKey(e => e.OrderId).HasName("orders_pkey");

            entity.Property(e => e.OrderDate).HasDefaultValueSql("now()");

            entity.HasOne(d => d.Customer).WithMany(p => p.Orders).HasConstraintName("orders_customer_id_fkey");
        });

        modelBuilder.Entity<OrderItem>(entity =>
        {
            entity.HasKey(e => e.OrderItemId).HasName("order_items_pkey");

            entity.HasOne(d => d.Order).WithMany(p => p.OrderItems).HasConstraintName("order_items_order_id_fkey");

            entity.HasOne(d => d.Product).WithMany(p => p.OrderItems).HasConstraintName("order_items_product_id_fkey");
        });

        modelBuilder.Entity<PaymentMethod>(entity =>
        {
            entity.HasKey(e => e.PaymentMethodId).HasName("payment_methods_pkey");

            entity.HasOne(d => d.Customer).WithMany(p => p.PaymentMethods).HasConstraintName("payment_methods_customer_id_fkey");
        });

        modelBuilder.Entity<Product>(entity =>
        {
            entity.HasKey(e => e.ProductId).HasName("products_pkey");

            entity.HasOne(d => d.Category).WithMany(p => p.Products).HasConstraintName("products_category_id_fkey");

            entity.HasMany(d => d.Categories).WithMany(p => p.ProductsNavigation)
                .UsingEntity<Dictionary<string, object>>(
                    "ProductCategory",
                    r => r.HasOne<Category>().WithMany()
                        .HasForeignKey("CategoryId")
                        .OnDelete(DeleteBehavior.ClientSetNull)
                        .HasConstraintName("product_categories_category_id_fkey"),
                    l => l.HasOne<Product>().WithMany()
                        .HasForeignKey("ProductId")
                        .OnDelete(DeleteBehavior.ClientSetNull)
                        .HasConstraintName("product_categories_product_id_fkey"),
                    j =>
                    {
                        j.HasKey("ProductId", "CategoryId").HasName("product_categories_pkey");
                        j.ToTable("product_categories");
                        j.IndexerProperty<int>("ProductId").HasColumnName("product_id");
                        j.IndexerProperty<int>("CategoryId").HasColumnName("category_id");
                    });
        });

        modelBuilder.Entity<ProductSupplier>(entity =>
        {
            entity.HasKey(e => new { e.ProductId, e.SupplierId }).HasName("product_suppliers_pkey");

            entity.HasOne(d => d.Product).WithMany(p => p.ProductSuppliers)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("product_suppliers_product_id_fkey");

            entity.HasOne(d => d.Supplier).WithMany(p => p.ProductSuppliers)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("product_suppliers_supplier_id_fkey");
        });

        modelBuilder.Entity<Reg>(entity =>
        {
            entity.HasKey(e => e.CustomerId).HasName("reg_pkey");
        });

        modelBuilder.Entity<Supplier>(entity =>
        {
            entity.HasKey(e => e.SupplierId).HasName("suppliers_pkey");
        });

        modelBuilder.Entity<Transaction>(entity =>
        {
            entity.HasKey(e => e.TransactionId).HasName("transactions_pkey");

            entity.Property(e => e.TransactionDate).HasDefaultValueSql("now()");

            entity.HasOne(d => d.Order).WithMany(p => p.Transactions).HasConstraintName("transactions_order_id_fkey");

            entity.HasOne(d => d.PaymentMethodNavigation).WithMany(p => p.Transactions).HasConstraintName("transactions_payment_method_id_fkey");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
