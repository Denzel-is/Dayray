using AdminDayray.Context;
using AdminDayray.Migrations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace AdminDayray.Controllers;

public class CustomersController : Controller
{
    private readonly MyDbContext _context;

    public CustomersController(MyDbContext context)
    {
        _context = context;
    }

  // Список клиентов
    public async Task<IActionResult> Index()
    {
        var customers = await _context.Regs.ToListAsync();
        return View(customers);
    }

    // Добавление клиента (GET)
    public IActionResult Create()
    {
        return View();
    }

    // Добавление клиента (POST)
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(Reg customer)
    {
        if (ModelState.IsValid)
        {
            _context.Regs.Add(customer);
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }
        return View(customer);
    }

    // Редактирование клиента (GET)
    public async Task<IActionResult> Edit(int? id)
    {
        if (id == null) return NotFound();

        var customer = await _context.Regs.FindAsync(id);
        if (customer == null) return NotFound();

        return View(customer);
    }

    // Редактирование клиента (POST)
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, Reg customer)
    {
        if (id != customer.CustomerId) return NotFound();

        if (ModelState.IsValid)
        {
            try
            {
                _context.Update(customer);
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!CustomerExists(customer.CustomerId))
                    return NotFound();
                else
                    throw;
            }
            return RedirectToAction(nameof(Index));
        }
        return View(customer);
    }

    // Удаление клиента (GET для подтверждения)
    public async Task<IActionResult> Delete(int? id)
    {
        if (id == null) return NotFound();

        var customer = await _context.Regs
            .FirstOrDefaultAsync(m => m.CustomerId == id);
        if (customer == null) return NotFound();

        return View(customer);
    }

    // Удаление клиента (POST)
    [HttpPost, ActionName("Delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteConfirmed(int id)
    {
        var customer = await _context.Regs.FindAsync(id);
        if (customer != null)
        {
            _context.Regs.Remove(customer);
            await _context.SaveChangesAsync();
        }
        return RedirectToAction(nameof(Index));
    }

    private bool CustomerExists(int id)
    {
        return _context.Regs.Any(e => e.CustomerId == id);
    }
}