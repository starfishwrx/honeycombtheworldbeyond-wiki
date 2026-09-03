const CANONICAL_ORIGIN = 'https://honeycombtheworldbeyond.wiki';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Enforce HTTPS and canonical apex on the custom domain
    if (url.hostname === 'www.honeycombtheworldbeyond.wiki' || (url.hostname === 'honeycombtheworldbeyond.wiki' && url.protocol !== 'https:')) {
      const canonical = new URL(url.pathname + url.search, CANONICAL_ORIGIN);
      return Response.redirect(canonical.toString(), 301);
    }

    return env.ASSETS.fetch(request);
  },
};
