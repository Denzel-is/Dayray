using System.Security.Claims;
using AdminDayray.Context;
using AdminDayray.Migrations;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Mvc;

namespace AdminDayray.Controllers;

public class AccountController : Controller
{
    private readonly MyDbContext _context;

    public AccountController(MyDbContext context)
    {
        _context = context;
    }

    // GET
    [HttpGet]
    public IActionResult Login()
    {
        return View();
    }

    [HttpPost]
    public async Task<IActionResult> Login(string username, string password)
    {
        var user = _context.Regs.SingleOrDefault(u => u.Username == username);

        if (user == null)
        {
            ModelState.AddModelError("", "Invalid username or password.");
            return View();
        }

        // Создание Claims
        var claims = new List<Claim>
        {
            new Claim(ClaimTypes.Name, user.Username),
            new Claim(ClaimTypes.Role, user.Role)
        };

        var claimsIdentity = new ClaimsIdentity(claims, "CookieAuth");
        var authProperties = new AuthenticationProperties
        {
            IsPersistent = true // Указывает, должна ли сессия быть постоянной
        };

        // Установка cookie
        await HttpContext.SignInAsync("CookieAuth", new ClaimsPrincipal(claimsIdentity), authProperties);

        return RedirectToAction("Index", "Home");
    }

  

    public async Task<IActionResult> Logout()
    {
        await HttpContext.SignOutAsync("CookieAuth");
        return RedirectToAction("Login");
    }

    public IActionResult AccessDenied()
    {
        return View();
    }
}