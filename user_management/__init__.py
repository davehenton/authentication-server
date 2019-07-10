import user_management.routes


def main(global_config, **settings):
    return routes.Route.load(**settings)
