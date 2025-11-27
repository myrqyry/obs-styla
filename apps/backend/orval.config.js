module.exports = {
  'obs-styla-frontend': {
    input: {
      target: './openapi.yaml',
    },
    output: {
      target: '../frontend/src/services/orval.ts',
      schemas: '../frontend/src/types/orval',
      client: 'react-query',
      mode: 'single',
      override: {
        mutator: {
          path: '../frontend/src/services/api.ts',
          name: 'apiMutator',
        },
      },
    },
    hooks: {
      useQuery: true,
      useMutation: true,
      useInfinite: false,
      useSuspenseQuery: false,
      useSuspenseInfiniteQuery: false,
    },
  },
  'obs-styla-web': {
    input: {
      target: './openapi.yaml',
    },
    output: {
      target: '../web/src/services/orval.ts',
      schemas: '../web/src/types/orval',
      client: 'react-query',
      mode: 'single',
      override: {
        mutator: {
          path: '../web/src/services/api.ts',
          name: 'apiMutator',
        },
      },
    },
    hooks: {
      useQuery: true,
      useMutation: true,
      useInfinite: false,
      useSuspenseQuery: false,
      useSuspenseInfiniteQuery: false,
    },
  },
};