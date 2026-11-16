import morph_kgc


def run(mapping, output):
    morph_kgc.materialize(f"[DataSource]\nmappings: rml/{mapping}").serialize(
        f"triples/{output}", format="nt"
    )


run("application.ttl", "applications_output.nt")
run("counties.ttl", "counties_output.nt")
run("fuel_source.ttl", "fuel_source_output.nt")
run("mec02.ttl", "mec02_output.nt")
run("mec03.ttl", "mec03_output.nt")
run("meg02.ttl", "meg02_output.nt")
run("months.ttl", "months_output.nt")
run("quarters.ttl", "quarters_output.nt")
run("wind_farms.ttl", "wind_farms_output.nt")
run("years.ttl", "years_output.nt")
