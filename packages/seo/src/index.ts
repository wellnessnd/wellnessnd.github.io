import { SUPPORTED_LOCALES, type LocalizedText, type Locale, type PublicProfile } from "@natali/profile";

export type SiteStatus = "draft" | "public";

export interface LocalizedPaths {
  ru: string;
  en: string;
  zh?: string;
  de?: string;
  fr?: string;
  es?: string;
}

export interface SeoInput {
  siteUrl: string;
  locale: Locale;
  paths: LocalizedPaths;
  status: SiteStatus;
}

export interface AlternateLink {
  hreflang: string;
  href: string;
}

function normalizeSiteUrl(value: string): string {
  const url = new URL(value);
  url.pathname = "/";
  url.search = "";
  url.hash = "";
  return url.toString();
}

export function absoluteUrl(siteUrl: string, path: string): string {
  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }
  return new URL(path.replace(/^\/+/, ""), normalizeSiteUrl(siteUrl)).toString();
}

export function buildSeo(input: SeoInput) {
  const currentPath = input.paths[input.locale] || input.paths.en || input.paths.ru;
  const canonical = absoluteUrl(input.siteUrl, currentPath);
  const alternates: AlternateLink[] = [];

  for (const [loc, path] of Object.entries(input.paths)) {
    if (path) {
      const locale = loc as Locale;
      alternates.push({
        hreflang: SUPPORTED_LOCALES[locale]?.sitemapLang || loc,
        href: absoluteUrl(input.siteUrl, path),
      });
    }
  }

  const defaultPath = input.paths.ru || input.paths.en;
  if (defaultPath) {
    alternates.push({ hreflang: "x-default", href: absoluteUrl(input.siteUrl, defaultPath) });
  }

  return {
    canonical,
    alternates,
    robots:
      input.status === "public"
        ? "index, follow, max-image-preview:large"
        : "noindex, nofollow, noarchive",
  };
}

export interface PersonJsonLdDetails {
  id?: string;
  url?: string;
  image?: string;
  jobTitle?: string;
  alternateName?: string;
  knowsAbout?: string[];
  sameAs?: string[];
  email?: string;
}

export function createPersonJsonLd(
  profile: PublicProfile,
  locale: Locale,
  pageUrl: string,
  details?: PersonJsonLdDetails,
) {
  const person: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "Person",
    "@id": details?.id || "https://orcid.org/0000-0003-0816-2103#person",
    name: profile.displayName[locale] || profile.displayName.en || profile.displayName.ru,
    url: details?.url || pageUrl,
    knowsLanguage: profile.languages,
  };

  if (details?.email) {
    person.email = details.email;
  }

  if (details?.image) {
    person.image = details.image;
  }
  if (details?.jobTitle) {
    person.jobTitle = details.jobTitle;
  }
  if (details?.alternateName) {
    person.alternateName = details.alternateName;
  }
  if (details?.knowsAbout && details.knowsAbout.length > 0) {
    person.knowsAbout = details.knowsAbout;
  }
  if (details?.sameAs && details.sameAs.length > 0) {
    person.sameAs = details.sameAs;
  }

  return person;
}

export interface BreadcrumbInputItem {
  label: string;
  /** Путь на том же сайте, например `/ru/about/`, или полный URL. Последний элемент может быть без href/path. */
  path?: string;
  href?: string;
  item?: string;
}

export function createBreadcrumbJsonLd(
  siteUrl: string,
  items: BreadcrumbInputItem[],
  currentPageUrl: string,
) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => {
      const rawTarget = item.path ?? item.href ?? item.item;
      const targetUrl = rawTarget
        ? absoluteUrl(siteUrl, rawTarget)
        : index === items.length - 1
          ? currentPageUrl
          : undefined;

      const element: Record<string, unknown> = {
        "@type": "ListItem",
        position: index + 1,
        name: item.label,
      };

      if (targetUrl) {
        element.item = targetUrl;
      }

      return element;
    }),
  };
}

export function createWebPageJsonLd(input: {
  name: string;
  description: string;
  url: string;
  locale: Locale;
  dateModified?: string;
  authorId?: string;
  authorName?: string;
}) {
  const page: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    name: input.name,
    description: input.description,
    url: input.url,
    inLanguage: input.locale,
    author: {
      "@type": "Person",
      "@id": input.authorId || "https://orcid.org/0000-0003-0816-2103#person",
      name: input.authorName || (input.locale === "ru" ? "Наталия Долгова" : input.locale === "zh" ? "娜塔莉亚·多尔戈娃 (Nataliia Dolgova)" : "Nataliia Dolgova"),
    },
  };
  if (input.dateModified) {
    page.dateModified = input.dateModified;
  }
  return page;
}

export function localizedValue(value: LocalizedText, locale: Locale): string {
  return value[locale] || value.en || value.ru || "";
}

export function formatUpdated(date: Date, locale: Locale): string {
  const localeTag = locale === "ru" ? "ru-RU" : locale === "zh" ? "zh-Hans" : locale === "de" ? "de-DE" : locale === "fr" ? "fr-FR" : locale === "es" ? "es-ES" : "en-GB";
  return new Intl.DateTimeFormat(localeTag, {
    dateStyle: "long",
    timeZone: "UTC",
  }).format(date);
}

export function formatMoney(
  amount: number,
  locale: Locale,
  options?: { maximumFractionDigits?: number },
): string {
  const localeTag = locale === "ru" ? "ru-RU" : locale === "zh" ? "zh-CN" : locale === "de" ? "de-DE" : locale === "fr" ? "fr-FR" : locale === "es" ? "es-ES" : "en-IE";
  return new Intl.NumberFormat(localeTag, {
    style: "currency",
    currency: "EUR",
    currencyDisplay: "symbol",
    maximumFractionDigits: options?.maximumFractionDigits ?? 0,
  }).format(amount);
}

export function robotsTxt(status: SiteStatus, siteUrl: string): string {
  if (status !== "public") {
    return "User-agent: *\nDisallow: /\n";
  }

  return [
    "# Traditional Search Engines & AI Search Crawlers (Allowed)",
    "User-agent: *",
    "Allow: /",
    "",
    "# AI Training Scrapers & Bulk Dataset Crawlers (Disallowed per DEC-AI-03)",
    "User-agent: GPTBot",
    "Disallow: /",
    "",
    "User-agent: CCBot",
    "Disallow: /",
    "",
    "User-agent: Google-Extended",
    "Disallow: /",
    "",
    "User-agent: anthropic-ai",
    "Disallow: /",
    "",
    "User-agent: ClaudeBot",
    "Disallow: /",
    "",
    `Sitemap: ${absoluteUrl(siteUrl, "/sitemap-index.xml")}`,
    "",
  ].join("\n");
}
