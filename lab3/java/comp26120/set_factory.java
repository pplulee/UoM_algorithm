package comp26120;

public class set_factory {
    speller_config config;
    
    public enum SetType {
        DARRAY,
        BSTREE,
        HASH
    }
    
    SetType set_type = SetType.DARRAY;
    
    public set_factory(SetType type, speller_config config) {
        set_type = type;
	this.config = config;
    }

    public set<String> initialise_set() {
        if (set_type == SetType.DARRAY) {
            return new darray(config);
	}
	else if (set_type == SetType.BSTREE) {
            return new bstree(config);
        } else {
            return new hashset(config);
	    } 
    }
    
}
