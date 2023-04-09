import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """  
    # print(people)
    # print(one_gene)
    # print(two_genes)
    # print(have_trait)
    joint_prob_single = [] 
    # probability of passing gene given no of genes
    two_pass = 1 - PROBS["mutation"] 
    one_pass = 0.5 
    zero_pass = PROBS["mutation"] 
    two_fail = 1 - two_pass
    one_fail = 1 - one_pass
    zero_fail = 1 - zero_pass 
    """for all peoples find joint probabiltiy distribution"""
    # consider all peoples
    for x in people: 
        #how many genes in x and is trait present
        if x in one_gene:
            no_of_genes = 1 
        elif x in two_genes:
            no_of_genes = 2
        else:
            no_of_genes = 0 
        if x in have_trait:
            is_trait = True
        else:
            is_trait = False 

        #mother father not given 
        if people[x]["mother"] == None and people[x]["father"] == None:
            p1 = PROBS["gene"][no_of_genes]                 # unconditional 

        #mother father given 
        else: 
            """if mother and father given then find conditional  probablity of p(no_of_genes|m_genes,g_genes) 
           using in following ways"""
            # no of genes in mother 
            if people[x]["mother"] in one_gene:
                m_genes = 1
            elif people[x]["mother"] in two_genes:
                m_genes = 2
            else :
                m_genes = 0 
            # no of genes in father
            if people[x]["father"] in one_gene:
                f_genes = 1
            elif people[x]["father"] in two_genes:
                f_genes = 2
            else:
                f_genes = 0
            #mother and father both have two genes 2 2 
            if m_genes == 2 and f_genes == 2:
               if no_of_genes == 2:
                   p1 = two_pass*two_pass 
               elif no_of_genes == 1:
                   p1 = two_fail*two_pass  
               else:
                   p1 = two_fail*two_fail 
            #mother and father have single single gene 0 2 or 2 0
            elif (m_genes ==  0 and f_genes == 2) or(m_genes == 2 and f_genes == 0):
               if no_of_genes == 2:
                   p1 = zero_pass*two_pass 
               elif no_of_genes == 1:
                   p1 = two_pass*zero_fail + zero_pass*two_fail
               else:
                   p1 = zero_fail*two_fail 
            # 0 1 or  1 0 
            elif ( m_genes == 1  and f_genes == 0) or (m_genes == 0 and f_genes == 1):
               if no_of_genes == 2:
                   p1 = one_pass*zero_pass
               elif no_of_genes == 1: 
                   p1 = one_pass*zero_fail + zero_pass*one_fail
               else:
                   p1 = zero_fail*one_fail 
            # 2 1 or 1 2 
            elif ( m_genes == 1  and f_genes == 2) or (m_genes == 2 and f_genes == 1):
               if no_of_genes == 2:
                   p1 = one_pass*two_pass 
               elif no_of_genes == 1:
                   p1 = two_pass*one_fail + one_pass*two_fail  
               else:
                   p1 = one_fail*two_fail 
            # 1 1
            elif ( m_genes == 1 and f_genes == 1): 
               if no_of_genes == 2:
                   p1 = one_pass*one_pass 
               elif no_of_genes == 1:
                    p1 = one_pass*one_fail 
               else:
                    p1 = one_fail*one_fail 
            # 0 0 
            elif m_genes == 0 and f_genes == 0:
               if no_of_genes == 2:
                   p1 = zero_pass*zero_pass
               elif no_of_genes == 1:
                   p1 = zero_pass*zero_fail
               else :
                   p1 = zero_fail*zero_fail         # conditional on mother and father genes 
        """p(gno,trait) = p(gno)*p(trait|gno)""" 
        """for child p(gno) == p(mgno,fgno,gno) , find using cases y*n + n*y"""
        p2 = PROBS["trait"][no_of_genes][is_trait]  # conditional  on gene no
        joint_p = p1*p2                             # joint
        joint_prob_single.append(joint_p) 

    total_joint_probability = 1
    for x in joint_prob_single :
        total_joint_probability *= x 
    return total_joint_probability 
    #raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """ 
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p 
    #print(probabilities)
    # raise NotImplementedError

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """ 
    """normalize by p(a) = p(a)/P(a)+p(b)""" 
    for person in probabilities:
        sum_of_gene_dist = probabilities[person]["gene"][0] + \
            probabilities[person]["gene"][1]+probabilities[person]["gene"][2] 
        sum_of_trait_dist = probabilities[person]["trait"][True] + \
            probabilities[person]["trait"][False] 
        for no in probabilities[person]["gene"]:
            probabilities[person]["gene"][no] /= sum_of_gene_dist 
        for iss in probabilities[person]["trait"]:
            probabilities[person]["trait"][iss] /= sum_of_trait_dist
    #print(probabilities) 
    # raise NotImplementedError


if __name__ == "__main__":
    main()
