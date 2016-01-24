main = """package <package>;
    
<imports>

public class <classname> extends Block {

    public <classname>() {
    super(Material.<material>);
    this.setCreativeTab(<creativeTab>);
    
    <singleTextureSrc>
}

<addAttributes>

<multiTextureSrc>

}"""

imports = """import net.minecraft.block.Block;
import net.minecraft.block.material.Material;"""

baseModSrc = """        <instancename> = new <classname>().setBlockName("<name>");
        GameRegistry.registerBlock(<instancename>, <instancename>.getUnlocalizedName().substring(5));"""
        
singleSidedTexture = """this.setBlockTextureName(<basemod>.MODID+":<texturename>");"""
    
multiSidedTexture = """    IIcon blockIconTop;
    IIcon blockIconBottom;
    IIcon blockIconFront;
    IIcon blockIconBack;
    IIcon blockIconLeft;
    IIcon blockIconRight;
    
    private static final String[][] textureTransformations = {{"Bottom", "Bottom", "Bottom", "Bottom", "Bottom", "Bottom"},
                                                              {"Bottom", "Top", "Top", "Top", "Top", "Top"},
                                                              {"Bottom", "Top", "Front", "Back", "Right", "Left"},
                                                              {"Bottom", "Top", "Back", "Front", "Left", "Right"},
                                                              {"Bottom", "Top", "Left", "Right", "Front", "Back"},
                                                              {"Bottom", "Top", "Right", "Left", "Back", "Front"}};
    
    @SideOnly(Side.CLIENT)
    @Override
    public void registerBlockIcons(IIconRegister p_149651_1_) {
        blockIconTop = p_149651_1_.registerIcon(<basemod>.MODID+":<texturename1>");
        blockIconBottom = p_149651_1_.registerIcon(<basemod>.MODID+":<texturename2>");
        blockIconFront = p_149651_1_.registerIcon(<basemod>.MODID+":<texturename3>");
        blockIconBack = p_149651_1_.registerIcon(<basemod>.MODID+":<texturename4>");
        blockIconLeft = p_149651_1_.registerIcon(<basemod>.MODID+":<texturename5>");
        blockIconRight = p_149651_1_.registerIcon(<basemod>.MODID+":<texturename6>");
    }

    public void onBlockAdded(World world, int x, int y, int z) {
		super.onBlockAdded(world, x, y, z);
		this.setDefaultDirection(world, x, y, z);
	}
	
	private void setDefaultDirection(World world, int x, int y, int z) {
       if (!world.isRemote) {
           Block block = world.getBlock(x, y, z - 1);
           Block block1 = world.getBlock(x, y, z + 1);
           Block block2 = world.getBlock(x - 1, y, z);
           Block block3 = world.getBlock(x + 1, y, z);
           byte b0 = 3;
            
           if (block.func_149730_j() && !block1.func_149730_j()) {
               b0 = 3;
           }
           if (block1.func_149730_j() && !block.func_149730_j()) {
               b0 = 2;
           }
           if (block2.func_149730_j() && !block3.func_149730_j()) {
               b0 = 5;
           }
           if (block3.func_149730_j() && !block2.func_149730_j()) {
               b0 = 4;
           }
            
           world.setBlockMetadataWithNotify(x, y, z, b0, 2);
       }
   }
	 
	public void onBlockPlacedBy(World world, int x, int y, int z, EntityLivingBase entityLivingBase, ItemStack itemstack) {
		int l = MathHelper.floor_double((double)(entityLivingBase.rotationYaw * 4.0F / 360.0F) + 0.5D) & 3;

	    	if (l == 0) {
	        	world.setBlockMetadataWithNotify(x, y, z, 2, 2);
	        }
	        if (l == 1) {
	        	world.setBlockMetadataWithNotify(x, y, z, 5, 2);
	        }
	        if (l == 2) {
	        	world.setBlockMetadataWithNotify(x, y, z, 3, 2);
	        }
	        if (l == 3) {
	        	world.setBlockMetadataWithNotify(x, y, z, 4, 2);
	        }

	   }

	@SideOnly(Side.CLIENT)
	public IIcon getIcon(int side, int metadata) {
		if (textureTransformations[metadata][side] == "Top") {
			return blockIconTop;
		} else {
		if (textureTransformations[metadata][side] == "Bottom") {
			return blockIconBottom;
		} else {
		if (textureTransformations[metadata][side] == "Front") {
			return blockIconFront;
		} else {
		if (textureTransformations[metadata][side] == "Back") {
			return blockIconBack;
		} else {
		if (textureTransformations[metadata][side] == "Left") {
			return blockIconLeft;
		} else {
		if (textureTransformations[metadata][side] == "Right") {
			return blockIconRight;
		}
		}
		}
		}
		}
		}
		
		return blockIconFront;
    }"""
    
transparent = """@Override
    public boolean isOpaqueCube() {
    	return false;
    }

    @Override
    public int getRenderBlockPass() {
    	return 0;
    }"""
    
additionalAttributes = {}