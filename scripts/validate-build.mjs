import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const failures = [];
const routes = {
  wellness: ["", "about", "for-individuals", "programs/stress-recovery", "practices/psychology", "practices/neurointegration", "practices/breathing", "practices/movement-qigong", "practices/play-and-story", "for-organizations", "resources", "booking", "faq"],
  science: ["", "about", "research", "research/dissertation", "publications", "conferences", "education", "projects", "expert-services", "for-organizations", "contact"],
};
const hreflangByLocale = {
  ru: "ru-RU",
  en: "en",
  zh: "zh-Hans",
  de: "de-DE",
  fr: "fr-FR",
  es: "es-ES",
};

for (const [site, siteRoutes] of Object.entries(routes)) {
  const siteLocales = site === "science" ? ["ru", "en", "zh", "de", "fr", "es"] : ["ru", "en"];
  for (const locale of siteLocales) {
    for (const route of siteRoutes) {
      const file = resolve(root, `apps/${site}/dist/${locale}/${route}/index.html`);
      if (!existsSync(file)) { failures.push(`Missing built route: ${site}/${locale}/${route || "home"}`); continue; }
      const html = readFileSync(file, "utf8");
      const expectedTokens = [
        locale === "zh" ? 'lang="zh-Hans"' : `lang="${locale}"`,
        "rel=\"canonical\"",
        `hreflang="${hreflangByLocale.ru}"`,
        `hreflang="${hreflangByLocale.en}"`,
        ...(site === "science" ? [
          `hreflang="${hreflangByLocale.zh}"`,
          `hreflang="${hreflangByLocale.de}"`,
          `hreflang="${hreflangByLocale.fr}"`,
          `hreflang="${hreflangByLocale.es}"`,
        ] : []),
        '"@type":"Person"',
        'id="main-content" tabindex="-1"',
        'content="nosniff"',
        'content="strict-origin-when-cross-origin"',
        'name="twitter:card"',
      ];
      for (const token of expectedTokens) {
        if (!html.includes(token)) failures.push(`${site}/${locale}/${route || "home"}: missing ${token}`);
      }
      if (html.includes('h4 class="footer-heading"')) {
        failures.push(`${site}/${locale}/${route || "home"}: obsolete h4 footer heading found`);
      }
      if (!html.includes('class="footer-cross-site"') && !html.includes("class='footer-cross-site'")) {
        failures.push(`${site}/${locale}/${route || "home"}: missing footer cross-site link`);
      }

      // Validate BreadcrumbList structured data if present
      const jsonLdRegex = /<script\s+type=["']application\/ld\+json["']>([\s\S]*?)<\/script>/gi;
      let jsonLdMatch;
      while ((jsonLdMatch = jsonLdRegex.exec(html)) !== null) {
        try {
          const parsed = JSON.parse(jsonLdMatch[1]);
          if (parsed["@type"] === "BreadcrumbList") {
            const list = parsed.itemListElement;
            if (!Array.isArray(list) || list.length === 0) {
              failures.push(`${site}/${locale}/${route || "home"}: BreadcrumbList itemListElement is empty or not an array`);
            } else {
              list.forEach((item, idx) => {
                if (item["@type"] !== "ListItem") {
                  failures.push(`${site}/${locale}/${route || "home"}: Breadcrumb item #${idx + 1} is not a ListItem`);
                }
                if (typeof item.position !== "number") {
                  failures.push(`${site}/${locale}/${route || "home"}: Breadcrumb item #${idx + 1} missing numeric position`);
                }
                if (!item.name || typeof item.name !== "string") {
                  failures.push(`${site}/${locale}/${route || "home"}: Breadcrumb item #${idx + 1} missing valid name`);
                }
                if (!item.item || typeof item.item !== "string" || !item.item.startsWith("http")) {
                  failures.push(`${site}/${locale}/${route || "home"}: Breadcrumb item #${idx + 1} (${item.name || 'unnamed'}) missing valid item URL: ${item.item}`);
                }
              });
            }
          }
        } catch (e) {
          failures.push(`${site}/${locale}/${route || "home"}: malformed JSON-LD: ${e.message}`);
        }
      }

      const distDir = resolve(root, `apps/${site}/dist`);
      const linkRegex = /<a\s+[^>]*?href=["']([^"']+)["']/gi;
      let match;
      while ((match = linkRegex.exec(html)) !== null) {
        const href = match[1];
        if (href.startsWith('/') && !href.startsWith('//')) {
          const cleanHref = href.split('#')[0].split('?')[0];
          if (cleanHref) {
            let target = resolve(distDir, cleanHref.replace(/^\/+/, ""));
            if (cleanHref.endsWith('/') || !cleanHref.includes('.')) target = resolve(target, 'index.html');
            if (!existsSync(target) && !existsSync(resolve(distDir, cleanHref.replace(/^\/+/, "")))) {
              failures.push(`${site}/${locale}/${route || "home"}: broken internal link: ${href}`);
            }
          }
        }
      }
    }
  }
}

for (const site of ["wellness", "science"]) {
  for (const sitemapFile of ["sitemap-index.xml", "sitemap-0.xml"]) {
    const sitemapPath = resolve(root, `apps/${site}/dist/${sitemapFile}`);
    if (!existsSync(sitemapPath)) failures.push(`${site}: missing ${sitemapFile}`);
  }
  const sitemap = readFileSync(resolve(root, `apps/${site}/dist/sitemap-0.xml`), "utf8");
  const origin = site === "wellness" ? "https://natalicompass.com" : "https://tvet.si";
  if (sitemap.includes(`<loc>${origin}/</loc>`)) {
    failures.push(`${site}: root noindex redirect must not appear in sitemap-0.xml`);
  }
  const sitemapLocales = site === "science" ? ["ru", "en", "zh", "de", "fr", "es"] : ["ru", "en"];
  for (const locale of sitemapLocales) {
    if (!sitemap.includes(`<loc>${origin}/${locale}/</loc>`)) {
      failures.push(`${site}: missing localized home in sitemap-0.xml: /${locale}/`);
    }
  }
  const rootIndex = resolve(root, `apps/${site}/dist/index.html`);
  if (!existsSync(rootIndex)) {
    failures.push(`${site}: missing root index.html`);
  } else {
    const rootHtml = readFileSync(rootIndex, "utf8");
    if (!rootHtml.includes('content="0;url=/en/"')) {
      failures.push(`${site}/index.html: missing fallback refresh content="0;url=/en/"`);
    }
    if (!rootHtml.includes('location.replace') || !rootHtml.includes('navigator.languages')) {
      failures.push(`${site}/index.html: missing client-side language detection script`);
    }
    if (!rootHtml.includes('href="/ru/"') || !rootHtml.includes('href="/en/"')) {
      failures.push(`${site}/index.html: missing localized fallback links`);
    }
    if (site === "science" && !rootHtml.includes('href="/zh/"')) {
      failures.push(`${site}/index.html: missing zh localized fallback link`);
    }
    if (site === "science" && !rootHtml.includes('href="/de/"')) {
      failures.push(`${site}/index.html: missing de localized fallback link`);
    }
    if (site === "science" && !rootHtml.includes('href="/fr/"')) {
      failures.push(`${site}/index.html: missing fr localized fallback link`);
    }
    if (site === "science" && !rootHtml.includes('href="/es/"')) {
      failures.push(`${site}/index.html: missing es localized fallback link`);
    }
  }
}

const sciencePublications = readFileSync(resolve(root, "apps/science/dist/en/publications/index.html"), "utf8");
for (const type of ["ScholarlyArticle", "Person", "WebPage"]) if (!sciencePublications.includes(`\"@type\":\"${type}\"`)) failures.push(`Science publications: missing ${type} structured data`);
const scienceProjects = readFileSync(resolve(root, "apps/science/dist/en/projects/index.html"), "utf8");
if (!scienceProjects.includes('"@type":"ResearchProject"')) failures.push("Science projects: missing ResearchProject structured data");

if (process.env.PUBLIC_SITE_STATUS === "public") {
  for (const [site, siteRoutes] of Object.entries(routes)) {
    const siteLocales = site === "science" ? ["ru", "en", "zh", "de", "fr", "es"] : ["ru", "en"];
    for (const locale of siteLocales) {
      for (const route of siteRoutes) {
        const file = resolve(root, `apps/${site}/dist/${locale}/${route}/index.html`);
        if (!existsSync(file)) continue;
        const html = readFileSync(file, "utf8");
        if (html.includes("draft-banner")) failures.push(`${site}/${locale}/${route || "home"}: draft banner must not appear in a public build`);
      }
    }
  }
}

for (const site of ["wellness", "science"]) {
  const file404 = resolve(root, `apps/${site}/dist/404.html`);
  if (!existsSync(file404)) {
    failures.push(`${site}: missing 404.html`);
  } else {
    const html404 = readFileSync(file404, "utf8");
    if (!html404.includes('content="noindex, nofollow"')) {
      failures.push(`${site}/404.html: missing content="noindex, nofollow"`);
    }
    if (html404.includes('rel="canonical"')) {
      failures.push(`${site}/404.html: canonical link must not appear on 404 page`);
    }
    if (html404.includes('property="og:url"')) {
      failures.push(`${site}/404.html: og:url must not appear on 404 page`);
    }
    if (html404.includes('hreflang=')) {
      failures.push(`${site}/404.html: alternate hreflang links must not appear on 404 page`);
    }
  }
}

if (failures.length) { console.error(failures.join("\n")); process.exitCode = 1; }
else console.log("Built-route validation passed for localized pages (including RU/EN/ZH/DE/FR/ES), canonical/hreflang, 404 SEO and structured data.");
