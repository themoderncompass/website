export const author = {
  name: 'Josh Imholte',
  alternateName: 'Joshua Imholte',
  id: 'https://themoderncompass.io/about#josh-imholte',
  url: 'https://themoderncompass.io/about',
  image: 'https://themoderncompass.io/1645116024072.jpeg',
  description: 'Author and creator of Modern Compass, and a product leader in tech.',
  sameAs: ['https://www.linkedin.com/in/josh-imholte/'],
};

export const authorSchema = {
  '@type': 'Person',
  '@id': author.id,
  name: author.name,
  alternateName: author.alternateName,
  url: author.url,
  image: author.image,
  description: author.description,
  sameAs: author.sameAs,
};

export const organizationId = 'https://themoderncompass.io/#organization';
